curl -XDELETE 'http://localhost:9200/mooc-courses/'
curl -XPUT 'http://localhost:9200/mooc-courses/'
curl -XPUT "http://localhost:9200/mooc-courses/edx/_mapping" -d '
{
    "_all" : {"enabled" : "true"},
    "properties" : { 
         "_id": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "school": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "name": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "faq": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "syllabus": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "start_time": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "about": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "platform": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "intro_url": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "description": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"}
    }
}'
curl -XPUT "http://localhost:9200/mooc-courses/xuetangx/_mapping" -d '
{
    "_all" : {"enabled" : "true"},
    "properties" : { 
         "_id": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "school": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "name": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "faq": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "syllabus": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "start_time": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "about": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "platform": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "intro_url": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "description": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"}
    }
}'
curl -XPUT "http://localhost:9200/mooc-courses/coursera/_mapping" -d '
{
    "_all" : {"enabled" : "true"},
    "properties" : { 
         "_id": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "school": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "name": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "faq": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "syllabus": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "start_time": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "about": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"},
         "platform": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "intro_url": {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
         "description": {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer": "ik"}
    }
}'
python indexer.py
