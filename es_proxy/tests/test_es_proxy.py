from tornado.httpserver import HTTPRequest

from ..functions import parse_request


SAMPLE_REQUEST_AND_PARSED_REQUEST = [
    {
        'description': 'Get information on the stats',
        'args': {
            'method': 'GET',
            'uri': '/_stats',
        },
        'parsed': {
            'call': '_stats', 'cluster': True, 'indices': [], 'scripted': False
        },
    },
]


def test_pytest():
    assert True, "This should always work."


def test_requests_to_parse_request():
    for sample in SAMPLE_REQUEST_AND_PARSED_REQUEST:
        tornado_http_request = HTTPRequest(**sample['args'])
        msg = "Problem with request: %s " % sample['description']
        assert parse_request(tornado_http_request) == sample['parsed'], msg
