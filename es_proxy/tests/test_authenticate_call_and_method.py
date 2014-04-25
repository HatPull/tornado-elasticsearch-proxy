from ..functions import authenticate_call_and_method


def test_authenticate_call_and_method_search_GET_with_index_read():
    """ The index_read permission authenticates _search with GET.
    """
    call = '_search'
    method = 'GET'

    test_policies = [
        {
            'resources': {
                'indices': ['joes_index', ],
            },
            'users': ['joe'],
            'permissions': ['index_read']
        },
    ]
    granted = authenticate_call_and_method(
        test_policies, call, method
    )

    assert granted


def test_authenticate_call_and_method_search_POST_mismatch_with_index_read():
    """ The index_read permission denies authentication for _search with POST.
    """
    call = '_search'
    method = 'POST'

    test_policies = [
        {
            'resources': {
                'indices': ['joes_index', ],
            },
            'users': ['joe'],
            'permissions': ['index_read']
        },
    ]
    granted = authenticate_call_and_method(
        test_policies, call, method
    )

    assert not granted


def test_authenticate_call_and_method_search_POST_mismatch_with_index_write():
    """ The index_read permission denies authentication for _search with POST.
    """
    call = '_search'
    method = 'GET'

    test_policies = [
        {
            'resources': {
                'indices': ['joes_index', ],
            },
            'users': ['joe'],
            'permissions': ['index_write']
        },
    ]
    granted = authenticate_call_and_method(
        test_policies, call, method
    )

    assert not granted
