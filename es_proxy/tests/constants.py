
SAMPLE_POLICIES = [
    {
        'scope': {
            'indices': ['kibana-int', ],
        },
        'users': ['*'],
        'permissions': ['index_write', 'index_read']
    },
    {
        'scope': {
            'cluster': True
        },
        'users': ['alan'],
        'permissions': ['kibana_admin', ]
    },
    {
        'scope': {
            'indices': ['joes_index', ],
        },
        'users': ['joe'],
        'permissions': ['index_write', 'index_read']
    },
    {
        'scope': {
            'indices': ['*', ],
        },
        'users': ['auditor', ],
        'permissions': ['index_read']
    },
]
