
from tornado.httpserver import HTTPRequest
import functions
from pprint import pprint

#Faking tornado HTTPRequest objects
#http://www.tornadoweb.org/en/stable/httpserver.html#httprequest-objects
#class tornado.httpserver.HTTPRequest(method, uri, version='HTTP/1.0', 
#                                     headers=None, body=None, remote_ip=None, 
#                                     protocol=None, host=None, files=None, connection=None)
#
#

SAMPLE_REQUESTS = [
    {
        #Get information on the stats
        'method' : 'GET',
        'uri' : '/_stats'
    },
    {
        #Search by GET
        'method' : 'GET',
        'uri' : '/twitter/tweet/_search?q=user:kimchy'
    },
    {
        #Create by PUT
        'method' : 'PUT',
        'uri' : '/twitter/tweet/1',
        'body' : '''{
                "user" : "kimchy",
                "post_date" : "2009-11-15T14:12:12",
                "message" : "trying out Elasticsearch"
            }'''
    },
    {
        #Search by GET, MULTI INDEX
        'method' : 'GET',
        'uri' : '/twitter,other_index,one_more_index/tweet/_search?q=user:kimchy'
    },
    {
        #Delete the articles index
        'method' : 'DELETE',
        'uri' : '/articles'
    },
    {
        #Create a new article
        'method' : 'POST',
        'uri' : '/articles/article',
        'body' : '{"title" : "Two",   "tags" : ["foo", "bar"]}'
    },
    {
        #Update via POST with script
        #Note that in the python heredoc syntax the backslashes have to be escaped 
        'method' : 'POST',
        'uri'    : '/test/type1/1/_update',
        'body'   : '''{
            "script" : "ctx._source.text = \\"some text\\""
            }'''
    },
    {
        #Update via POST without script 
        'method' : 'POST',
        'uri'    : '/test/type1/1/_update',
        'body'   : '''{
                "doc" : {
                    "name" : "new_name"
                }
            }'''
    },
    {
        #Query by POST
        'method' : 'POST',
        'uri' : '/articles/_search?pretty=true',
        'body' : ''' {
                "query" : { "query_string" : {"query" : "T*"} },
                "facets" : {
                  "tags" : { "terms" : {"field" : "tags"} }
                }
            }
            '''
    },
    {
        #Query by POST with script_fields
        'method' : 'GET',
        'uri' : '/articles/_search?pretty=true',
        'body' : ''' {
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
    }
]


print
print '######################### PARSE REQUEST ##########################'
print

for request_args in SAMPLE_REQUESTS:
    tornado_http_request = HTTPRequest(**request_args)
    print
    print "uri: %s" % request_args['uri']
    # if 'body' in request_args.keys():
    #     print request_args['body']
    pprint(functions.parse_request(tornado_http_request))
    print


SAMPLE_POLICIES = [
    { 
        'scope' : {
            'indices' : ['kibana-int'],
         },
        'users' : ['*'],
        'permissions' : ['index_write', 'index_read']
    },
    {   
        'scope' : {
            'cluster' : True
        },
        'users' : ['alan'],
        'permissions' : ['kibana_admin']
    },
    {   
        'scope' : {
            'indices' : ['joes_index'],
        },
        'users' : ['joe'],
        'permissions' : ['index_write', 'index_read']
    }
]   


print
print '######################### SCOPE POLICIES ##########################'
print 

#Test a few scenarios for scope
print "For index kibana-int"
cluster = False
indices = ['kibana-int']
scope_policies = functions.get_scope_available_policies(cluster, indices, SAMPLE_POLICIES)
pprint(scope_policies)
print

print "For non existing index not_index"
cluster = False
indices = ['not_index']
scope_policies = functions.get_scope_available_policies(cluster, indices, SAMPLE_POLICIES)
pprint(scope_policies)
print

print "Cluster"
cluster = True
indices = []
scope_policies = functions.get_scope_available_policies(cluster, indices, SAMPLE_POLICIES)
pprint(scope_policies)
print

print
print '######################### USER POLICIES ##########################'
print 

print "User: joe"
#Test a few policies for users
user = 'joe'
user_policies = functions.get_user_available_policies(user, SAMPLE_POLICIES)
pprint(user_policies)
print

print "User: bob"
#Test a few policies for users
user = 'bob'
user_policies = functions.get_user_available_policies(user, SAMPLE_POLICIES)
pprint(user_policies)
print
