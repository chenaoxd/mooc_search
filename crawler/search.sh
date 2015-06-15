curl -XGET 'http://localhost:9200/mooc-courses/_search?pretty' -d '
{
        "query": {
            "query_string": {
                "fields": ["_all"],
                "query": "Introduction to Astronomy"
            }
        },
        "size": "100"
}'
