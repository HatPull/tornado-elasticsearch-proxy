import json

with open('/opt/env.json') as infile:
    env = json.load(infile)


LISTEN_PORT = int(env['ES_PROXY_LISTEN_PORT'])

# Permissions is a list of matrices
# Each matrix is the defined by the possible calls and the possible methods
# A user may be granted a set of permissions either
# on the cluster or on a particular index or indices.
PERMISSIONS = {
    # Home is considered the elasticsearch root or "/"
    'home_read': {
        'allow_calls': ['_home'],
        'allow_methods': ['GET'],
        'allow_script': False
    },
    # Global Admin permission, allows all calls and methods
    'admin': {
        'allow_calls': '*',
        'allow_methods': '*',
        'allow_script': False
    },
    # Global Admin read permission, allows all calls,
    # but just GET and HEAD methods
    'admin_read': {
        'allow_calls': '*',
        'allow_methods': ['GET', 'HEAD'],
        'allow_script': False
    },
    # Kibana admin - Kibana needs some permissions to
    # get information about the server and indices
    'kibana_admin': {
        'allow_calls': '_nodes,',
        'allow_methods': ['GET', 'HEAD'],
        'allow_script': False
    },
    #The basic calls and methods needed to read or search and index, or indices
    'index_read': {
        'allow_calls': ['_document', '_query', '_search'],
        'allow_methods': ['GET', 'HEAD'],
        'allow_script': False
    },
    #The basic calls and methods needed to write to and index, or indices
    'index_write': {
        'allow_calls': ['_document', '_create'],
        'allow_methods': ['PUT', 'POST'],
        'allow_script': False
    },
}

ELASTICSEARCH = {
    'url': 'http://%s:%s' % (env['ES_PORT_9200_TCP_ADDR'], env['ES_PORT_9200_TCP_PORT']),
    'auth_mode': 'basic',  # uses curl_httpclient can be basic or digest
    'auth_username': '',
    'auth_password': '',
}

#permissions get granted to users on resources based on policies
POLICIES = [
    # All users have access to the kibana internal index
    # a resource could be indices/aliases/cluster
    {
        'indices': ['kibana-int', ],
        'users': ['*'],
        'permissions': ['index_write', 'index_read']
    },
    #Kibana needs to know about the cluster _nodes
    {
        'cluster': True,
        'users': ['*'],
        'permissions': ['kibana_admin']
    },
    # sample
    {
        'indices': ['sample_index', ],
        'users': ['sample_user'],
        'permissions': ['index_read']
    },

]

#Ignore any requests for these paths
IGNORE_PATHS = [
    '/favicon.ico'
]
