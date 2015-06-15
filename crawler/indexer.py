# coding=utf-8
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['mooc_search']
course_col = db['courses']

if __name__ == '__main__':
    print __file__, 'running..'
    for course in course_col.find():
        print course
