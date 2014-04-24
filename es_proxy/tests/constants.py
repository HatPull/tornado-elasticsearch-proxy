
SAMPLE_POLICIES = [
    {
        'resources': {
            'indices': ['kibana-int', ],
        },
        'users': ['*'],
        'permissions': ['index_write', 'index_read']
    },
    {
        'resources': {
            'cluster': True
        },
        'users': ['alan'],
        'permissions': ['kibana_admin', ]
    },
    {
        'resources': {
            'indices': ['joes_index', ],
        },
        'users': ['joe'],
        'permissions': ['index_write', 'index_read']
    },
    {
        'resources': {
            'indices': ['*', ],
        },
        'users': ['auditor', ],
        'permissions': ['index_read']
    },
]
