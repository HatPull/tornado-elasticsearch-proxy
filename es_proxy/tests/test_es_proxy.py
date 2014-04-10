from tornado.httpserver import HTTPRequest

from ..functions import parse_request


SAMPLE_REQUEST_AND_PARSED_REQUEST = [
    {
        # Get information on the stats
        'args': {
            'method': 'GET',
            'uri': '/_stats',
        },
        'parsed': {
            'call': '_stats', 'cluster': True, 'indices': [], 'scripted': False
        },
    },
    {
        # Search by GET
        'args': {
            'method': 'GET',
            'uri': '/twitter/tweet/_search?q=user:kimchy',
        },
        'parsed': {
            'call': '_search',
            'cluster': False,
            'indices': ['twitter'],
            'scripted': False
        }
    },
    {
        # Create by PUT
        'args': {
            'method': 'PUT',
            'uri': '/twitter/tweet/1',
            'body': '''{
                    "user" : "kimchy",
                    "post_date" : "2009-11-15T14:12:12",
                    "message" : "trying out Elasticsearch"
                }'''
        },
        'parsed': {
            'call': '_document',
            'cluster': False,
            'indices': ['twitter'],
            'scripted': False
        }
    },
    {
        #Search by GET, MULTI INDEX
        'args': {
            'method': 'GET',
            'uri': '/twitter,index1,index2/tweet/_search?q=user:kimchy'
        },
        'parsed': {
            'call': '_search',
            'cluster': False,
            'indices': ['twitter', 'index1', 'index2'],
            'scripted': False
        }
    },
    {
        #Delete the articles index
        'args': {
            'method': 'DELETE',
            'uri': '/articles'
        },
        'parsed': {
            'call': '_document',
            'cluster': False,
            'indices': ['articles'],
            'scripted': False
        }
    },
    {
        # Create a new article
        'args': {
            'method': 'POST',
            'uri': '/articles/article',
            'body': '{"title" : "Two",   "tags" : ["foo", "bar"]}'
        },
        'parsed': {
            'call': '_document',
            'cluster': False,
            'indices': ['articles'],
            'scripted': False
        }
    },
    {
        # Update via POST with script
        'args': {
            'method': 'POST',
            'uri': '/test/type1/1/_update',
            # Note that in the python heredoc syntax
            # the backslashes have to be escaped
            'body': '''{
                "script" : "ctx._source.text = \\"some text\\""
                }'''
        },
        'parsed': {
            'call': '_update',
            'cluster': False,
            'indices': ['test'],
            'scripted': True
        }
    },
    {
        #Update via POST without script
        'args': {
            'method': 'POST',
            'uri': '/test/type1/1/_update',
            'body': '''{
                    "doc" : {
                        "name" : "new_name"
                    }
                }'''
        },
        'parsed': {
            'call': '_update',
            'cluster': False,
            'indices': ['test'],
            'scripted': False
        }
    },

]


def test_pytest():
    assert True, "This should always work."


def test_requests_to_parse_request():
    for sample in SAMPLE_REQUEST_AND_PARSED_REQUEST:
        tornado_http_request = HTTPRequest(**sample['args'])
        assert parse_request(tornado_http_request) == sample['parsed']
