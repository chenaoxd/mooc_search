# coding=utf-8
import pymongo
import requests
import json
import urllib
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['mooc_search']
course_col = db['courses']

def remove_course_tags(course):
    course['mongo_id'] = course['_id']
    course['_id'] = course['_id'].replace('/', '_').replace(':', '_')
    course['description'] = BeautifulSoup(course['description']).get_text()
    course['about'] = BeautifulSoup(course['about']).get_text()
    course['faq'] = BeautifulSoup(course['faq']).get_text()
    course['syllabus'] = BeautifulSoup(course['syllabus']).get_text()

    for a in course:
        if type(a) == 'unicode':
            course[a] = course[a].encode('utf-8')
    return course

if __name__ == '__main__':
    print __file__, 'running..'
    for course in course_col.find(timeout=False):
        course = remove_course_tags(course)
        #print course
        r = requests.request('post', 'http://127.0.0.1:9200/mooc-courses/%s/%s' % (course['platform'], urllib.quote_plus(course['_id'])), data=json.dumps(course, ensure_ascii=False).encode('utf-8'))
        print r.text
