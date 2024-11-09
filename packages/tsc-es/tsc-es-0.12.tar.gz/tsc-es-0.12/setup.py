# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

if os.path.exists('readme.md'):
    long_description = open('readme.md', 'r', encoding='utf8').read()
else:
    long_description = ''

setup(
    name='tsc-es',
    version='0.12',
    description="mongo to es",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='tsc',
    license='GPLv3',
    url='',
    keywords='tools',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'elasticsearch',
        'tqdm',
        'pymongo',
        'pytz',
        'requests',
    ],
    python_requires='>=3.7',
)
