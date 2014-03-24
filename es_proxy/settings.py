import json

with open('/home/docker/env.json') as infile:
    env = json.load(infile)

#Permissions is a list of matrices
#Each matrix is the defined by the possible calls and the possible methods
#A user may be granted a set of permissions either on the cluster or on a particular index
#or indices
PERMISSIONS =  {
    #Home is considered the elasticsearch root or "/"
    'home_read' : {   
        'allow_calls' : ['_home'],
        'allow_methods' : ['GET']
    },
    #Global Admin permission, allows all calls and methods
    'admin' : {   
        'allow_calls' : '*',
        'allow_methods' : '*'
    }, 
    #Global Admin read permission, allows all calls, but just GET and HEAD methods
    'admin_read' : {   
        'allow_calls' : '*',
        'allow_methods' : ['GET', 'HEAD']
    },
    #Kibana admin read - Kibana needs some permissions to get information about the server
    #and indices
    'kibana_admin_read' : {   
        'allow_calls' : '_nodes,',
        'allow_methods' : ['GET', 'HEAD']
    },
    #The basic calls and methods needed to read or search and index, or indices
    'index_user_read' : {   
        'allow_calls' : ['_document', '_query', '_search'],
        'allow_methods' : ['GET', 'HEAD'], 
    },
    #The basic calls and methods needed to write to and index, or indices
    'index_user_write' : {   
        'allow_calls' : ['_document',],
        'allow_methods' : ['PUT', 'POST']
    },
}
           
ELASTICSEARCH =  {
    'url' :  'http://%s:%s' % (env['ES_PORT_9200_TCP_ADDR'], env['ES_PORT_9200_TCP_PORT']),
    'auth_mode' : 'basic', #uses curl_httpclient can be basic or digest
    'auth_username' : '',
    'auth_password' : '',
}

#permissions get granted to users in a scope based on policies
POLICIES = [
    #All users have access to the kibana internal index
    #scope could be indexes/aliases/cluster
    { 'scope' : ['index:kibana-int'],
      'users' : ['*'],
      'permissions' : ['index_user_write', 'index_user_read']
    },
    #Kibana needs to know about the cluster _nodes
    { 'scope' : ['cluster'],
      'users' : ['*'],
      'permissions' : ['kibana_admin_read']
    }
]   
        
    