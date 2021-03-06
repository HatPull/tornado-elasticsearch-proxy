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
        'calls': ['_home', ],
        'methods': ['GET', ],
        'script': False
    },
    # Global Admin permission, allows all calls and methods
    'admin': {
        'calls': '*',
        'methods': '*',
        'script': False
    },
    # Global Admin read permission, allows all calls,
    # but just GET and HEAD methods
    'admin_read': {
        'calls': '*',
        'methods': ['GET', 'HEAD', ],
        'script': False
    },
    # Kibana admin - Kibana needs some permissions to
    # get information about the server and indices
    'kibana_admin': {
        'calls': '_nodes,',
        'methods': ['GET', 'HEAD', ],
        'script': False
    },
    # The basic calls and methods needed to search an index, or indices
    'index_search': {
        'calls': ['_search'],
        'methods': ['GET', 'POST', ],
        'script': False
    },
    # The basic calls and methods needed to read or query an index, or indices
    'index_read': {
        'calls': ['_document', '_query', ],
        'methods': ['GET', 'HEAD', ],
        'script': False
    },
    # The basic calls and methods needed to write to and index, or indices
    'index_write': {
        'calls': ['_document', '_create', ],
        'methods': ['PUT', 'POST', ],
        'script': False
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
