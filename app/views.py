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

def search_course(request):
    res = {}
    query = request.GET.get('query', '')
    res['query'] = query
    if query == '':
        response = json.loads(requests.request('get', 'http://127.0.0.1:9200/mooc-courses/_search').text)
        search_results = response['hits']['hits']
    else:
        response = json.loads(requests.request('get', 'http://127.0.0.1:9200/mooc-courses/_search?q=%s' % urllib.quote_plus(query.encode('utf-8'))).text)
        search_results = response['hits']['hits']

    final_results = []
    for r in search_results:
        if r['_source']['start_time'] or True:
            final_results.append(r)
            
            if type(r['_source']['school']) == type([]):
                r['_source']['school'] = r['_source']['school'][0]
            if r['_source']['img_url'].startswith('/'):
                if r['_source']['platform'] == 'xuetangx':
                    r['_source']['img_url'] = 'http://www.xuetangx.com' + r['_source']['img_url']
            r['_source']['name'] = BeautifulSoup(r['_source']['name']).get_text()
    res['courses'] = final_results
    res['error'] = error(1, 'ok')
    return HttpResponse(json.dumps(res), content_type = 'application/json')
