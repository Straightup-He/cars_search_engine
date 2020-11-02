from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from app01.utils.pagination import Pagination
from elasticsearch import Elasticsearch

# 连接es
es = Elasticsearch(['127.0.0.1:9200'])

# 首页
def index(request):
    if request.method == 'GET':
        body = {
            "query": {
                "match": {
                    "tag": "news"
                }
            },
            "from": 0,
            "size": 10
        }
        res = es.search(index="cars", doc_type="doc", body=body)['hits']['hits']
        news_dict = [{
            "title": item['_source']['title'],
            "title_url": item['_source']['title_url'],
            "desc": item['_source']['desc'],
        } for item in res]
        return render(request, 'index.html', {"news_dict": news_dict})
    else:
        msg = request.POST.get('msg')
        tag = request.POST.get('tag')
        current_page = request.POST.get('current_page')  #获取当前页码
        res = search_data(msg, tag, current_page)
        return JsonResponse(res)


# 到es过滤数据并返回给前端
def search_data(msg, tag, current_page):
    """ 到es过滤数据并返回给前端 """
    if tag != 'all':
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "title": msg
                            }
                        },
                        {
                            "term": {
                                "tag": {
                                    "value": tag
                                }
                            }
                        }
                    ]
                }
            },
            "from": 0,
            "size": 10000,
            "highlight": {
                "pre_tags": "<b style='color:lightpink;'>",
                "post_tags": "</b>",
                "fields": {
                    "title": {}
                }
            }
        }
    else:
        body = {
            "query": {
                "match": {
                    "title": msg
                }
            },
            "from": 0,
            "size": 10000,
            "highlight": {
                "pre_tags": "<b style='color:lightpink;'>",
                "post_tags": "</b>",
                "fields": {
                    "title": {}
                }
            }
        }
    res = es.search(index='cars', doc_type='doc', body=body)
    # 数据总数
    total_count = res['hits']['total']
    pagination = Pagination(page_num=current_page, total_count=total_count)
    print(pagination.start_data_num,pagination.end_data_num)
    custom_dict = dict(
        total_count=res['hits']['total'],
        data_msg=res['hits']['hits'][pagination.start_data_num:pagination.end_data_num],
        page_msg=pagination.pagination_html()
    )
    print(custom_dict['data_msg'])
    return custom_dict

# ---------------以下是建议器部分------------------
# 接收被建议的内容
def advice(request):
    if request.method == 'POST':
        input_msg = request.POST.get("input_msg").strip()
        if input_msg:
            search_advice(input_msg)
            return JsonResponse(search_advice(input_msg))
        else:
            return JsonResponse({"error": 0})

# 到es搜索数据并返回建议
def search_advice(input_msg):
    """到es搜索数据并返回建议"""
    body = {
        "suggest": {
            "text": input_msg,
            "my_term_suggest": {
                "term": {
                    "field": "word",
                    "size": 3
                }
            },
            "my_phrase_suggest": {
                "phrase": {
                    "field": "word",
                    "size": 3,
                    "highlight": {
                        "pre_tag": "<b style='color: red;'>",
                        "post_tag": "</b>"
                    }
                }
            },
            "my_completion_suggest": {
                "completion": {
                    "field": "word",
                    "size": 3
                }
            }
        }
    }
    res = es.search(index='words', doc_type='doc', body=body)['suggest']
    es_advice = []
    # 完成建议器
    if res['my_completion_suggest'][0]['options']:
        for item in res['my_completion_suggest'][0]['options']:
            es_advice.append(item['_source']['word'])
    # term建议器
    if res['my_term_suggest']:
        for item in res['my_term_suggest'][0]['options']:
            es_advice.append(item['text'])
    # phrase建议器
    if res['my_phrase_suggest'][0]['options']:
        for item in res['my_phrase_suggest'][0]['options']:
            es_advice.append(item['highlighted'])

    return {"es_advice": es_advice}
