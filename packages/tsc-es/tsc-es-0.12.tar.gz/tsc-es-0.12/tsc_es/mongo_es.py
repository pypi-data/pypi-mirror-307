import logging
from elasticsearch.helpers import parallel_bulk
from elasticsearch import Elasticsearch, ConflictError, NotFoundError
from collections import deque
from pprint import pprint
from tqdm import tqdm
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from datetime import timedelta, datetime
import pytz
import argparse
import time
import traceback
from typing import Optional, Union, Literal


def get(key, obj, default=None):
    """
    递归从dict/list/tuple中取值, 以list的形式，以避免中括号取值数量不灵活的问题
    :param key: list/tuple/int/str; list表示递归取值
    :param obj: dict/list/tuple
    :param default: 寻找不到后返回的默认值
    :return:
    """
    key = key if isinstance(key, list) else [key]
    if len(key) == 0:
        return obj
    for i in key:
        try:
            obj = obj[i]
        except:
            obj = default
            break
    return obj


def get_properties_and_processors_from_map_fields(
    map_fields: dict[str, dict],
    mmdb: Optional[str] = None,
) -> tuple[dict[str, dict], list[dict]]:
    """
    从 map_fields 中获取 properties 和 processors
    :param map_fields: 映射字段
    :param mmdb: geo信息使用的 database_file, None代表使用默认 (一般是 GeoLite2-City.mmdb / GeoIP2-City.mmdb)
    :return: properties, processors
    """
    properties: dict[str, dict] = {}
    processors: list[dict] = []
    for k, v in map_fields.items():
        properties[k] = {"type": v['es_type']}
        if v['es_type'] == 'text':
            properties[k].update({
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_smart",
                **({"fields": {
                    "keyword": {
                        "type": "keyword",
                    }
                }} if v.get('es_keyword', False) else {}),
            })
        if v['es_type'] == 'date':
            properties[k].update({
                "format": "date_optional_time||epoch_millis"
            })
        if v['es_type'] == 'ip':
            kk = f'{k}_geo'
            assert kk not in map_fields
            geos = ['IP', 'COUNTRY_ISO_CODE', 'COUNTRY_NAME', 'CONTINENT_NAME', 'REGION_ISO_CODE', 'REGION_NAME', 'CITY_NAME', 'TIMEZONE', 'LOCATION']
            properties[kk] = {
                "properties": {
                    geo.lower(): { "type": "geo_point" if geo=='LOCATION' else 'keyword' } for geo in geos
                }
            }
            processors += [
                {
                    "geoip": {
                        "field": k,
                        "target_field": kk,
                        "properties": geos,
                        "ignore_missing": True,
                        **({"database_file": mmdb} if mmdb else {}),
                    }
                },
            ]
        if v.get('es_options'):
            assert 'type' not in v['es_options'], 'type should not be in es_options'
            properties[k].update(v['es_options'])
    return properties, processors


def creat_template(
    client: Elasticsearch,
    name: str,
    index_patterns: list[str],
    map_fields: dict[str, dict],
    is_stream: bool = False,
    number_of_shards: int = 4,
    mmdb: Optional[str] = None,
    number_of_replicas: int = 0,
    analysis: Optional[dict] = None,
    dynamic: Literal['true', 'runtime', 'false', 'strict'] = 'false',
    dynamic_templates: Optional[list[dict]] = None,
) -> bool:
    """
    创建 es 模版, 可能会新建同名管道
    :param client: es 客户端
    :param name: 模版名称
    :param index_patterns: 允许的索引名称列表
    :param map_fields: 映射字段
    :param is_stream: 是否是 date_stream 索引
    :param number_of_shards: 分片数量
    :param mmdb: geo信息使用的 database_file, None代表使用默认 (一般是 GeoLite2-City.mmdb / GeoIP2-City.mmdb)
    :param number_of_replicas: 副本数量
    :param analysis: 分析器设置
    :param dynamic: 是否允许动态添加字段，否则写入时未定义的字段不会加入索引
    :param dynamic_templates: 动态模板
    :return: 是否成功
    """
    if client.indices.exists_index_template(name=name):
        logging.debug(f"Template '{name}' exists.")
        return False
    print('index num:', len(map_fields))
    pprint({k: v.get('note') for k, v in map_fields.items()})
    properties, processors = get_properties_and_processors_from_map_fields(map_fields, mmdb)
    # 创建管道
    pipeline_id = name
    try:
        pipeline = client.ingest.get_pipeline(id=pipeline_id)
        logging.debug(f"pipeline '{pipeline_id}' exists.")
    except Exception as e:
        ingest_pipeline_body = {
            "description": pipeline_id,
            "processors": processors
        }
        ret = client.ingest.put_pipeline(id=pipeline_id, body=ingest_pipeline_body)
        logging.warning(f"pipeline '{pipeline_id}' is created: {ret}")
    # 创建模版
    index_template_body = {
        "index_patterns": index_patterns, 
        "template": {
            "settings": {
                "number_of_shards": number_of_shards,  # 分片数量
                "number_of_replicas": number_of_replicas,  # 副本数量
                "analysis": analysis or {
                    "analyzer": {
                        "default": {
                            "type": "ik_smart",
                        }
                    }
                },
                "default_pipeline": pipeline_id,
            },
            "mappings": {
                "properties": properties,
                "dynamic": dynamic,
                "dynamic_templates": dynamic_templates or [],
            },
        },
    }
    if is_stream:
        index_template_body['data_stream'] = {}
    # pprint(index_template_body)
    ret = client.indices.put_index_template(name=name, **index_template_body)
    logging.warning(f"Template '{name}' is created: {ret}")
    return True


def create_index(client: Elasticsearch, name: str, is_stream=False):
    """
    创建索引. 索引创建以后就和模版无关了，管道还是相关的
    :param client: es 客户端
    :param name: 索引名称
    :param is_stream: 是否是 date_stream 索引
    :return: 是否成功
    """
    if is_stream:
        # 数据流只能是create, 会对数据更新和es_bulk带来麻烦
        if check_data_stream_exists(client, name):
            logging.debug(f"Stream_name '{name}' exists.")
            return False
        else:
            ret = client.indices.create_data_stream(name=name)
            logging.warning(f"Stream_name '{name}' is created: {ret}")
            return True
    else:
        # 索引
        if client.indices.exists(index=name):
            logging.debug(f"index '{name}' exists.")
            return False
        else:
            ret = client.indices.create(index=name)
            logging.warning(f"index '{name}' is created: {ret}")
            return True


def update_template_indexes(
    client: Elasticsearch,
    name: str,
    map_fields: dict[str, dict],
    mmdb: Optional[str] = None,
) -> bool:
    """
    更新 ES 模版以添加新字段，同时更新管道和现有索引。只能增加字段，不能删改字段
    :param client: es 客户端
    :param name: 模版名称
    :param map_fields: 修改后的映射字段
    :param mmdb: geo信息使用的 database_file, None代表使用默认 (一般是 GeoLite2-City.mmdb / GeoIP2-City.mmdb)
    :return: 是否成功
    """
    try:
        # 获取当前模板信息
        template = client.indices.get_index_template(name=name)
        current_template = template['index_templates'][0]['index_template']
        current_properties: dict[str, dict] = current_template['template']['mappings']['properties']
        
        # 找出增量字段
        deleted_map_fields = {k: v for k, v in current_properties.items() if k not in map_fields}
        if deleted_map_fields:
            logging.error(f"Can not delete fields in template '{name}': {deleted_map_fields}")
            return False
        new_map_fields = {k: v for k, v in map_fields.items() if k not in current_properties}
        if not new_map_fields:
            logging.debug(f"No new fields in template '{name}'.")
            return False
        added_properties, processors = get_properties_and_processors_from_map_fields(new_map_fields, mmdb)
        
        # 更新管道
        pipeline_id = name
        if processors:
            try:
                existing_pipeline = client.ingest.get_pipeline(id=pipeline_id)
                # 添加新的 processors 到现有 pipeline 的 processors 列表中
                existing_pipeline[pipeline_id]['processors'].extend(processors)
                client.ingest.put_pipeline(id=pipeline_id, body=existing_pipeline[pipeline_id])
                logging.debug(f"pipeline '{pipeline_id}' is updated with new processors.")
            except Exception as e:
                logging.error(f"Failed to update pipeline '{pipeline_id}': {e}")
                return False
        
        # 更新模板的 properties
        current_properties.update(added_properties)
        # 使用现有模板结构直接更新
        ret = client.indices.put_index_template(name=name, **current_template)
        logging.warning(f"Template '{name}' is updated with new fields: {list(new_map_fields)}")
        
        # 更新已有索引
        matching_indices = []
        for pattern in current_template['index_patterns']:
            matching_indices.extend(client.indices.get(index=pattern).keys())
        
        for index_name in matching_indices:
            client.indices.put_mapping(index=index_name, properties=added_properties)
            logging.info(f"Index '{index_name}' is updated with new fields.")
        
        return True

    except Exception as e:
        logging.error(f"Failed to update template '{name}': {e}")
        return False


def check_data_stream_exists(client: Elasticsearch, name):
    """
    判断 data_stream 类型的索引是否存在
    :param client: es 客户端
    :param name: 索引名称
    :return: 是否成功
    """
    data_streams = client.indices.get_data_stream(name='*')
    for ds in data_streams['data_streams']:
        if ds['name'] == name:
            return True
    return False


def del_template(client: Elasticsearch, name: str):
    """
    删除 es 索引模版, 会尝试删除同名管道, 需要关联的 index 先删除
    :param client: es 客户端
    :param name: 模版名称
    :return: 
    """
    try:
        client.ingest.delete_pipeline(id=name)
        logging.warning(f'pipeline {name} del')
    except NotFoundError:
        ...
    try:
        client.indices.delete_index_template(name=name)
        logging.warning(f'template {name} del')
    except NotFoundError:
        ...


def del_index(client: Elasticsearch, name: str, is_stream=False):
    """
    删除 es 索引
    :param client: es 客户端
    :param name: 索引名称
    :param is_stream: 是否是 date_stream 索引
    :return: 
    """
    try:
        if is_stream:
            client.indices.delete_data_stream(name=name)
            logging.warning(f'data_stream {name} del')
        else:
            client.indices.delete(index=name)
            logging.warning(f'index {name} del')
    except NotFoundError:
        ...


def es_bulk(
    client: Elasticsearch,
    name: str,
    data: list[dict],
    op_type: Literal['index', 'update', 'delete'] = 'index',
    raise_on_error: bool = True,
):
    """
    批量索引数据
    :param client: es 客户端
    :param name: 索引名称
    :param data: 待索引的数据
    :param op_type: 索引类型
    :param raise_on_error: 在插入一条出现错误的时候是否报错, False 表示继续插入下一条
    :return: 
    """
    logging.debug('op_type:'+op_type+' ,number is:' + str(len(data)))
    
    def generate_actions():
        for item in data:
            assert '_id' in item
            if op_type == 'index' or op_type == 'create':
                yield {
                    '_op_type': op_type,
                    "_index": name,
                    **item,
                }
            elif op_type == 'update':
                yield {
                    '_op_type': op_type,
                    "_index": name,
                    "_id": item.pop('_id'),
                    "doc": item
                }
            elif op_type == 'delete':
                yield {
                    '_op_type': op_type,
                    "_index": name,
                    "_id": item['_id'],
                }
    success_num = 0
    for success, info in parallel_bulk(client=client, actions=generate_actions(),
                        chunk_size=3000, thread_count=8, raise_on_error=raise_on_error):
        if not success or info.get('index', {}).get('status') == 409:
            logging.info('A document failed: ' + str(info))
        else:
            success_num += 1
    return success_num


def get_docs_from_cursor(cursor: Cursor, map_fields: dict, batch_size=500, get_id=None, doc_skip_f=None):
    """
    从 mongo 的cursor中构建es需要的索引格式
    :param cursor: 游标
    :param map_fields: 映射字段
    :param batch_size: 每次返回的doc数量
    :param get_id: 函数, 输入doc返回_id, 如果为None表示直接返回doc中的_id
    :param doc_skip_f: 函数, 输入doc返回是否跳过这个doc, 如果为None表示不跳过
    :return: [doc,..]
    """
    batch = []
    get_id = (lambda doc: str(doc['_id'])) if get_id is None else get_id
    for item in cursor:
        if doc_skip_f is not None and doc_skip_f(item):
            continue
        try:
            doc = {k: v.get('opt', lambda x: x)(get(v['keys'], item, v['default'])) for k, v in map_fields.items()}
        except:
            print(item)
            raise
        batch.append({
            '_id': get_id(item),
            **doc,
        })
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def mongo_to_es(client: Elasticsearch, index_name: str, collection: Collection, map_fields: dict,
          time_field_es: str, time_field_mongo: str, mongo_is_date=False, timestamp_tz='Asia/Shanghai',
          doc_skip_f=None, get_id=None, batch_size=500, is_stream=False, raise_on_error=True, op_type='index',
          mongo_filter: dict=None, es_filter: list=None):
    """
    从 mongo 导入到 es
    :param client: es 客户端
    :param index_name: 索引名称
    :param collection: mongo 的集合
    :param map_fields: 映射字段
    :param time_field_es: es 中的时间字段, 用于增量更新
    :param time_field_mongo: mongo 中的时间字段, 用于增量更新
    :param mongo_is_date: time_field_mongo 是否为 date 类型, 否则代表是精确到微秒的秒级时间戳
    :param timestamp_tz: time_field_mongo 为时间戳时候的时区
    :param doc_skip_f: 参见 get_docs_from_cursor
    :param get_id: 参见 get_docs_from_cursor
    :param batch_size: 参见 get_docs_from_cursor
    :param is_stream: 是否是 date_stream 索引
    :param raise_on_error: 在插入一条出现错误的时候是否报错, False 表示不管这个错误继续插入下一条
    :param op_type: 索引类型, data stream 会自动修改为 create
    :param mongo_filter: 一些针对 collection 进行的额外过滤, 以便于同步一部分. 要与 es_filter 配合
        例子: {'source_db_summary.source_id': {'$exists': False}}
    :param es_filter: 一些针对 index_name 进行的额外过滤, 以便于同步一部分. 要与 mongo_filter 配合
        例子: [{'term': {'source_summary_id.keyword': ''}}]
    :return: 
    """
    op_type = 'create' if is_stream else op_type
    body = {
        "size": 1,
        "query": {
            "bool": {
                'must': [{"match_all": {}}],
                "filter": es_filter if es_filter else [],
            }
        },
        "sort": {
            time_field_es: {"order": "desc"},
        },
    }
    es_res = client.search(index=index_name, **body)
    start_time = None
    if es_res['hits']['hits'] and es_res['hits']['hits'][0]['_source'][time_field_es]:
        start_time = es_res['hits']['hits'][0]['_source'][time_field_es]
        if isinstance(start_time, str):  # 精确到毫秒的日期
            start_time = datetime.strptime(start_time, r"%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.UTC)
            if mongo_is_date:
                start_time = start_time + timedelta(milliseconds=1)
            else:  # 需要确保 mongo 中的时间戳的时区是当地时区
                start_time = start_time.timestamp() + 0.001
        else:
            start_time += 1e-6  # 要求是精确到微秒的秒级时间戳
            if mongo_is_date:
                start_time = datetime.fromtimestamp(start_time, tz=pytz.timezone(timestamp_tz))
    logging.info(str(start_time))
        
    mongo_filter = mongo_filter if mongo_filter else {}
    if start_time:
        mongo_filter[time_field_mongo] = {'$gte': start_time}
    info = collection.find(mongo_filter).sort(time_field_mongo, ASCENDING)
    info_count = collection.count_documents(mongo_filter)
    ret = {
        'time_field_es': time_field_es,
        'time_field_mongo': time_field_mongo,
        'find_num': info_count,
        'success_num': 0,
    }
    
    if info_count:
        pbar = tqdm(total=info_count, desc='更新中', unit='个文档', leave=False)
        for upsert_data_L in get_docs_from_cursor(info, map_fields=map_fields, doc_skip_f=doc_skip_f,
                                                  get_id=get_id, batch_size=batch_size):
            if not upsert_data_L:
                continue
            if is_stream and raise_on_error:
                for doc in upsert_data_L:
                    _id = doc.pop('_id')
                    try:
                        client.create(index=index_name, id=_id, document=doc)
                        ret['success_num'] += 1
                    except ConflictError:
                        continue
                    except:
                        print(_id, doc)
                        raise
                    pbar.update(1)
            else:
                ret['success_num'] += es_bulk(client, index_name, upsert_data_L, op_type=op_type, raise_on_error=raise_on_error)
                pbar.update(len(upsert_data_L))
        pbar.close()

    if ret['success_num']:
        logging.warning(str(ret))
    else:
        logging.info(str(ret))
    return ret


def time_to_es_date(
    t: Union[float, int, datetime],
    from_utc=False,
    current_tz=pytz.timezone('Asia/Shanghai'),
):
    """
    将时间转换成 es 的 date 类型
    :param t: float or datetime; 时间戳或日期类型
    :param from_utc: 是否是utc时间, 来自mongo的date需要设置 from_utc=Ture
    :param current_tz: 如果不是utc时间, 那么其时区是什么
    :return: str
    """
    if t is None or t == '':
        return None
    # 转换时间戳为 datetime 对象, 保证是已经被 current_tz 格式的
    if isinstance(t, (int, float)):
        try:
            dt = datetime.fromtimestamp(t, tz=pytz.utc if from_utc else current_tz)
        except ValueError:
            logging.warning(f'try to convert milliseconds: {t} -> {t/1000}')
            t /= 1000
            dt = datetime.fromtimestamp(t, tz=pytz.utc if from_utc else current_tz)
    else:
        dt = t
    # 将本地时间转换为 UTC 时间
    if not from_utc:
        # dt = dt.replace(tzinfo=current_tz)  # 这会导致减少 6 分钟
        dt = dt.astimezone(pytz.utc)
    # 转换 datetime 对象为 Elasticsearch 日期格式
    es_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return es_date


def es_date_to_datetime(es_date: str, from_utc=True, current_tz=pytz.timezone('Asia/Shanghai')):
    """
    es 的 date 类型转换成 datetime 时间
    :param es_date: es 的 date 类型时间
    :param from_utc: 是否是utc时间, 一般都是
    :param current_tz: 如果不是utc时间, 那么其时区是什么
    :return: datetime
    """
    # 转换为Python的datetime对象，并设置为UTC时区
    utc_datetime = datetime.strptime(es_date, r"%Y-%m-%dT%H:%M:%S.%fZ")
    # 转换为北京时间
    if from_utc:
        utc_datetime = utc_datetime.replace(tzinfo=pytz.UTC)
        utc_datetime = utc_datetime.astimezone(current_tz)
    return utc_datetime


def define_map_fields():  # 例子
    return {
        'record_date': {  # es索引名
            'keys': ['record_time'],  # get 提取
            'default': None,  # 默认的提取值
            'es_type': 'date',  # 对应的es类型, 例如 date/boolean/float/integer/long/text/keyword/ip/doubole/dense_vector
            'opt': lambda x: time_to_es_date(x),  # 提取doc之后的再处理
            'note': '入库时间',  # 注释
        },
        'text': {  # 
            'keys': ['text'],
            'default': None,
            'es_type': 'text',
            'es_keyword': True,  # 针对 text 类型可以选择是否将该文本当关键词处理形成 text.keyword 字段
            'es_options': {},  # 额外的 es 字段设置, 例如 {"index": False} 表示不索引，还可以是 text 的 analyzer/search_analyzer，或者 dense_vector 的 dims/similarity 等
            'note': '',
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", default='WARNING', help="日志等级, 例如 INFO, WARNING")
    parser.add_argument('--delete', action='store_true', help='是否先删除已有索引')
    args = parser.parse_args()
    log_format = '%(asctime)s %(levelname)s - %(message)s'
    logging.basicConfig(level=args.level, format=log_format)  # INFO WARNING
    
    index_name = 'test'  # 索引名称
    template_name = index_name
    index_patterns = [index_name]
    
    client = Elasticsearch(['url',], basic_auth=('user', 'passwd'))
    
    # node_info = client.nodes.info()
    # for node_id, node_data in node_info["nodes"].items():
    #     print(f"Node ID: {node_id}")
    #     print(f"Name: {node_data['name']}")
    #     print(f"Roles: {node_data['roles']}")
    #     print("=" * 30)
    
    map_fields=define_map_fields()
    if args.delete:
        del_index(client, index_name)
        del_template(client, template_name)
    creat_template(client, template_name, index_patterns=index_patterns, map_fields=map_fields)
    create_index(client, index_name)

    while True:
        try:
            info = mongo_to_es(client, index_name, Collection(), map_fields, 'record_time', 'record_time')
        except:
            traceback.print_exc()
        time.sleep(10)
