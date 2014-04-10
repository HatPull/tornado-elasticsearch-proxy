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
        'args': {
            # Create by PUT
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

]


def test_pytest():
    assert True, "This should always work."


def test_requests_to_parse_request():
    for sample in SAMPLE_REQUEST_AND_PARSED_REQUEST:
        tornado_http_request = HTTPRequest(**sample['args'])
        assert parse_request(tornado_http_request) == sample['parsed']
