# -*- coding = utf-8 -*-
# @Time : 2020/9/26 22:12
# @Author : straightup
"""
批量写入数据

"""

import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# 连接es
es = Elasticsearch(['127.0.0.1:9200'])

# 记录时间的装饰器
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('共耗时{:.2f}秒'.format(time.time() - start))
        return res

    return wrapper


@timer
def create_word_data():
    """创建单词的索引"""
    body = {
        "mappings": {
            "doc": {
                "dynamic": "strict",
                "properties": {
                    "word": {
                        "type": "completion",
                        "analyzer": "ik_smart",
                        "preserve_separators": "true",
                        "preserve_position_increments": "true",
                        "max_input_length": 50
                    }
                }
            }
        }
    }
    es.indices.create(index='words', body=body)
    print("ok")

@timer
def insert_word_data():
    """使用生成器批量写入数据"""
    with open('spider/word.txt', 'r', encoding='utf-8', errors='ignore') as f:
        action = ({
            "_index": "words",
            "_type": "doc",
            "_source": {"word": line.strip()}
        } for line in f)
        helpers.bulk(es, actions=action)


# 查询单词
def select():
    while 1:
        result = input(">>>:").strip()
        if result.lower() == 'q':
            break
        print(es.search(index='words', doc_type='doc', body={
            "query": {
                "match": {
                    "word": result
                }
            }
        }))


# 创建汽车之家数据组织
@timer
def create_car_data():
    """创建汽车之家数据组织"""
    body = {
        "mappings": {
            "doc": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "ik_smart",
                    },
                    "title_url": {"type": "keyword", "index": "false"},
                    "desc": {"type": "keyword", "index": "false"},
                    "tag": {"type": "keyword"},
                    "img_url": {"type": "keyword", "index": "false"}
                }
            }
        }
    }
    es.indices.create(index='cars', body=body)
    print("ok")


# 插入汽车之家数据
@timer
def insert_car_data():
    """ 插入汽车之家数据 """
    with open('spider/car2.txt', 'r', encoding='utf-8', errors='ignore') as f:
        action = ({
            "_index": "cars",
            "_type": "doc",
            "_source": {
                "title": line.strip().split('|')[0],
                "title_url": line.strip().split('|')[1],
                "desc": line.strip().split('|')[2],
                "tag": line.strip().split('|')[3],
                "img_url": line.strip().split('|')[4]
            }
        } for line in f)
        helpers.bulk(es, actions=action)


if __name__ == '__main__':
    # create_word_data()
    # insert_word_data()
    select()
    # create_car_data()
    # insert_car_data()
