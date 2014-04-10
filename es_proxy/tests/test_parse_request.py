from tornado.httpserver import HTTPRequest

from ..functions import parse_request


def test_get_stats():
    """ Test parse_request for 'Get information on the stats
        returns correctly parsed request.
    """

    request = {
        'args': {
            'method': 'GET',
            'uri': '/_stats',
        },
        'parsed_request': {
            'call': '_stats', 'cluster': True, 'indices': [], 'scripted': False
        },
    }
    tornado_http_request = HTTPRequest(**request['args'])
    assert parse_request(tornado_http_request) == request['parsed_request']


def test_get_search():
    """ Test parse_request for 'Search by GET'
        returns correctly parsed request.
    """

    request = {
        # Search by GET
        'args': {
            'method': 'GET',
            'uri': '/twitter/tweet/_search?q=user:kimchy',
        },
        'parsed_request': {
            'call': '_search',
            'cluster': False,
            'indices': ['twitter'],
            'scripted': False
        }
    }

    tornado_http_request = HTTPRequest(**request['args'])
    assert parse_request(tornado_http_request) == request['parsed_request']


def test_create_by_put():
    """ Test parse_request for 'Create by PUT'
        returns correctly parsed request.
    """

    request = {
        'args': {
            'method': 'PUT',
            'uri': '/twitter/tweet/1',
            'body': '''{
                    "user" : "kimchy",
                    "post_date" : "2009-11-15T14:12:12",
                    "message" : "trying out Elasticsearch"
                }'''
        },
        'parsed_request': {
            'call': '_document',
            'cluster': False,
            'indices': ['twitter'],
            'scripted': False
        }
    }

    tornado_http_request = HTTPRequest(**request['args'])
    assert parse_request(tornado_http_request) == request['parsed_request']


def test_search_by_multi_index_get():
    """ Test parse_request for 'Search by GET, MULTI INDEX'
        returns correctly parsed request.
    """

    request = {
        'args': {
            'method': 'GET',
            'uri': '/twitter,index1,index2/tweet/_search?q=user:kimchy'
        },
        'parsed_request': {
            'call': '_search',
            'cluster': False,
            'indices': ['twitter', 'index1', 'index2'],
            'scripted': False
        }
    }

    tornado_http_request = HTTPRequest(**request['args'])
    assert parse_request(tornado_http_request) == request['parsed_request']


def test_delete_index():
    """ Test parse_request for 'Delete the articles index'
        returns correctly parsed request.
    """

    request = {
        'args': {
            'method': 'DELETE',
            'uri': '/articles'
        },
        'parsed_request': {
            'call': '_document',
            'cluster': False,
            'indices': ['articles'],
            'scripted': False
        }
    }

    tornado_http_request = HTTPRequest(**request['args'])
    assert parse_request(tornado_http_request) == request['parsed_request']


def test_create_document_with_post():
    """ Test parse_request for 'Create a new article document with POST'
        returns correctly parsed request.
    """

    request = {
        'args': {
            'method': 'POST',
            'uri': '/articles/article',
            'body': '{"title" : "Two",   "tags" : ["foo", "bar"]}'
        },
        'parsed_request': {
            'call': '_document',
            'cluster': False,
            'indices': ['articles'],
            'scripted': False
        }
    }

    tornado_http_request = HTTPRequest(**request['args'])
    assert parse_request(tornado_http_request) == request['parsed_request']


def test_update_document_with_script():
    """ Test parse_request for 'Update via POST with script'
        returns correctly parsed request.
    """

    request = {
        'args': {
            'method': 'POST',
            'uri': '/test/type1/1/_update',
            # Note that in the python heredoc syntax
            # the backslashes have to be escaped
            'body': '''{
                "script" : "ctx._source.text = \\"some text\\""
                }'''
        },
        'parsed_request': {
            'call': '_update',
            'cluster': False,
            'indices': ['test'],
            'scripted': True
        }
    }

    tornado_http_request = HTTPRequest(**request['args'])
    assert parse_request(tornado_http_request) == request['parsed_request']


def test_update_document_without_script():
    """ Test parse_request for 'Update via POST without script
        returns correctly parsed request.
    """

    request = {
        'args': {
            'method': 'POST',
            'uri': '/test/type1/1/_update',
            'body': '''{
                    "doc" : {
                        "name" : "new_name"
                    }
                }'''
        },
        'parsed_request': {
            'call': '_update',
            'cluster': False,
            'indices': ['test'],
            'scripted': False
        }
    }

    tornado_http_request = HTTPRequest(**request['args'])
    assert parse_request(tornado_http_request) == request['parsed_request']


def test_query_by_post():
    """ Test parse_request for 'Query via POST without script fields
        returns correctly parsed request.
    """

    request = {
        'args': {
            'method': 'POST',
            'uri': '/articles/_search?pretty=true',
            'body': ''' {
                    "query" : { "query_string" : {"query" : "T*"} },
                    "facets" : {
                      "tags" : { "terms" : {"field" : "tags"} }
                    }
                }
                '''
        },
        'parsed_request': {
            'call': '_search',
            'cluster': False,
            'indices': ['articles'],
            'scripted': False
        }
    }

    tornado_http_request = HTTPRequest(**request['args'])
    assert parse_request(tornado_http_request) == request['parsed_request']


def test_query_by_post_with_script_fields():
    """  Query via POST with script fields
        returns correctly parsed request.
    """

    request = {
        'args': {
            'method': 'GET',
            'uri': '/articles/_search?pretty=true',
            'body': ''' {
                    "query" :  { "query_string" : {"query" : "T*"} },
                    "script_fields" : {
                        "test1" : {
                            "script" : "doc['my_field_name'].value * 2"
                        },
                        "test2" : {
                            "script" : "doc['my_field_name'].value * factor",
                            "params" : {
                                "factor"  : 2.0
                            }
                        }
                    }
                }
                '''
        },
        'parsed_request': {
            'call': '_search',
            'cluster': False,
            'indices': ['articles'],
            'scripted': True
        }
    }

    tornado_http_request = HTTPRequest(**request['args'])
    assert parse_request(tornado_http_request) == request['parsed_request']
