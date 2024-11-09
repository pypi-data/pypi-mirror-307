import requests
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Optional, Any


def get_roles(
    es_host: str,
    admin_user: str,
    admin_password: str,
) -> Dict[str, Any]:
    """
    获取所有角色的详细信息。

    :param es_host: Elasticsearch 实例的主机地址（例如：http://localhost:9200）。
    :param admin_user: 管理员用户名，用于认证请求。
    :param admin_password: 管理员密码，用于认证请求。
    :return: 包含所有角色信息的字典。每个角色的名称作为字典的键，角色详细信息作为值。
    """
    url = f"{es_host}/_security/role"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers,
                            auth=HTTPBasicAuth(admin_user, admin_password))
    return response.json()


def get_users(
    es_host: str,
    admin_user: str,
    admin_password: str,
) -> Dict[str, Any]:
    """
    获取所有用户的详细信息。

    :param es_host: Elasticsearch 实例的主机地址（例如：http://localhost:9200）。
    :param admin_user: 管理员用户名，用于认证请求。
    :param admin_password: 管理员密码，用于认证请求。
    :return: 包含所有用户信息的字典。每个用户名作为字典的键，用户详细信息作为值。
    """
    url = f"{es_host}/_security/user"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers,
                            auth=HTTPBasicAuth(admin_user, admin_password))
    return response.json()


def create_role(
    es_host: str,
    admin_user: str,
    admin_password: str,
    role_name: str,
    indices: List[str],
    privileges: List[str]
) -> dict:
    """
    创建一个角色，赋予指定的索引和权限。

    :param es_host: Elasticsearch 实例的主机地址（例如：http://localhost:9200）。
    :param admin_user: 管理员用户名，用于认证请求。
    :param admin_password: 管理员密码，用于认证请求。
    :param role_name: 要创建的角色名称。
    :param indices: 索引名称列表，定义该角色有权限访问的索引。
    :param privileges: 权限列表，为角色分配的权限，例如 ['read', 'write']。
    :return: Role Creation Response
    """
    url = f"{es_host}/_security/role/{role_name}"
    data = {
        "indices": [
            {
                "names": indices,
                "privileges": privileges
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, json=data, headers=headers,
                            auth=HTTPBasicAuth(admin_user, admin_password))
    return response.json()


def create_user(
    es_host: str,
    admin_user: str,
    admin_password: str,
    username: str,
    password: str,
    roles: List[str],
    full_name: Optional[str] = "",
    email: Optional[str] = ""
) -> dict:
    """
    创建一个用户并分配角色。

    :param es_host: Elasticsearch 实例的主机地址（例如：http://localhost:9200）。
    :param admin_user: 管理员用户名，用于认证请求。
    :param admin_password: 管理员密码，用于认证请求。
    :param username: 要创建的用户名。
    :param password: 为用户设置的密码。
    :param roles: 该用户分配的角色列表。
    :param full_name: 用户的全名（可选）。
    :param email: 用户的邮箱地址（可选）。
    :return: User Creation Response
    """
    url = f"{es_host}/_security/user/{username}"
    data = {
        "password": password,
        "roles": roles,
        "full_name": full_name,
        "email": email
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url, json=data, headers=headers, auth=HTTPBasicAuth(admin_user, admin_password))
    return response.json()


def change_user_password(
    es_host: str,
    admin_user: str,
    admin_password: str,
    username: str,
    new_password: str,
) -> dict:
    """
    修改指定用户的密码。

    :param es_host: Elasticsearch 实例的主机地址（例如：http://localhost:9200）。
    :param admin_user: 管理员用户名，用于认证请求。
    :param admin_password: 管理员密码，用于认证请求。
    :param username: 要修改密码的用户名。
    :param new_password: 为用户设置的新密码。
    :return: Password Change Response
    """
    url = f"{es_host}/_security/user/{username}/_password"
    data = {
        "password": new_password
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url, json=data, headers=headers, auth=HTTPBasicAuth(admin_user, admin_password))
    return response.json()


def update_role(
    es_host: str,
    admin_user: str,
    admin_password: str,
    role_name: str,
    indices: Optional[List[str]] = None,
    privileges: Optional[List[str]] = None
) -> dict:
    """
    修改指定角色的权限和索引。如果未提供新索引或权限，则保持原有配置。

    :param es_host: Elasticsearch 实例的主机地址（例如：http://localhost:9200）。
    :param admin_user: 管理员用户名，用于认证请求。
    :param admin_password: 管理员密码，用于认证请求。
    :param role_name: 要更新的角色名称。
    :param indices: 新的索引名称列表，定义该角色有权限访问的索引（可选）。
    :param privileges: 新的权限列表，为角色分配的权限，例如 ['read', 'write']（可选）。
    :return: None
    """
    url = f"{es_host}/_security/role/{role_name}"

    # 构建请求数据
    data = {}
    if indices or privileges:
        data["indices"] = [
            {
                "names": indices if indices else [],
                "privileges": privileges if privileges else []
            }
        ]

    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, json=data, headers=headers,
                            auth=HTTPBasicAuth(admin_user, admin_password))
    return response.json()


def update_user_roles(
    es_host: str,
    admin_user: str,
    admin_password: str,
    username: str,
    roles: List[str]
) -> dict:
    """
    修改指定用户的角色。

    :param es_host: Elasticsearch 实例的主机地址（例如：http://localhost:9200）。
    :param admin_user: 管理员用户名，用于认证请求。
    :param admin_password: 管理员密码，用于认证请求。
    :param username: 要更新角色的用户名。
    :param roles: 新的角色列表，将分配给该用户。
    :return: None
    """
    url = f"{es_host}/_security/user/{username}"
    data = {
        "roles": roles
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.put(
        url, json=data, headers=headers, auth=HTTPBasicAuth(admin_user, admin_password))
    return response.json()
