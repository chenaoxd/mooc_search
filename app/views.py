# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from models import error
from bs4 import BeautifulSoup

import json
import requests
import urllib

# Create your views here.

def index(request):
    request.META["CSRF_OOKIE_USED"] = True
    context = {
        'role': request.session.get('role', 1)
    }
    return render_to_response('index.html', RequestContext(request, context))

def test(request):
    return HttpResponse('test')

def translate_query(query):
    response = json.loads(requests.request('get', 'http://fanyi.youdao.com/openapi.do?keyfrom=sfdsfsf&key=1999761367&type=data&doctype=json&version=1.1&q=%s' % urllib.quote_plus(query.encode('utf-8'))).text)
    #print json.dumps(response)
    translations = []
    translation_set = set()
    weight = 0.9
    for a in response['translation']:
        a = a.lower()
        translations.append((a, weight))
        translation_set.add(a)
        weight *= 0.5

    if 'web' not in response:
        return translations
        
    weight = 0.45
    for a in response['web'][0]['value']:
        a = a.lower()
        if a not in translation_set:
            translations.append((a, weight))
        weight *= 0.5
    return translations

def search_course(request):
    def merge_results(list1, list2, weight):
        ''
        for a in list2:
            #print a['_source']['name'], a['_score'] * weight
            if a['_id'] in result_set:
                continue
            result_set.add(a['_id'])
            a['_score'] = a['_score'] * weight
            list1.append(a)
        list1 = sorted(list1, key = lambda a:a['_score'], reverse=True)
        return list1
    
    res = {}
    query = request.GET.get('query', '')
    if not query:
        query = '信息检索'
    res['query'] = query
    result_set = set()
    
    if query == '':
        response = json.loads(requests.request('get', 'http://127.0.0.1:9200/mooc-courses/_search').text)
        search_results = response['hits']['hits']
        result_set.update([a['_id'] for a in search_results])
    else:
        translations = translate_query(query)
        response = json.loads(requests.request('get', 'http://127.0.0.1:9200/mooc-courses/_search?q=%s' % urllib.quote_plus(query.encode('utf-8'))).text)
        search_results = response['hits']['hits']
        result_set.update([a['_id'] for a in search_results])

        for trans_tu in translations:
            trans = trans_tu[0]
            #print trans
            response = json.loads(requests.request('get', 'http://127.0.0.1:9200/mooc-courses/_search?q=%s' % urllib.quote_plus(trans.encode('utf-8'))).text)
            trans_search_results = response['hits']['hits']
            search_results = merge_results(search_results, trans_search_results, trans_tu[1])

    final_results = []
    for r in search_results:
        if r['_source']['img_url']:
            final_results.append(r)
                    
            r['_source']['name'] = BeautifulSoup(r['_source']['name']).get_text()
    res['courses'] = final_results
    res['error'] = error(1, 'ok')
    return HttpResponse(json.dumps(res), content_type = 'application/json')
