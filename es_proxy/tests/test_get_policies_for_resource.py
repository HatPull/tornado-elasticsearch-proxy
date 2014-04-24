from ..functions import get_policies_for_resource

from .constants import SAMPLE_POLICIES


def test_get_policies_for_resource_for_index_kibana_int():
    """ For index kibana-int. """
    cluster = False
    indices = ['kibana-int']
    scope_policies = get_policies_for_resource(
        cluster, indices, SAMPLE_POLICIES
    )

    expected_scope_policies = [
        {
            'permissions': ['index_write', 'index_read'],
            'scope': {'indices': ['kibana-int']},
            'users': ['*']
        }
    ]

    assert scope_policies == expected_scope_policies


def test_get_policies_for_resource_with_bad_policy():
    """ Testing get_policies_for_resource
        with bad scope key.
    """

    BAD_POLICY = [
        {
            'scope': {'weird_key': ['*']},
            'users': ['*']
        }
    ]
    cluster = False
    indices = None
    scope_policies = get_policies_for_resource(
        cluster, indices, BAD_POLICY
    )

    expected_scope_policies = []

    assert scope_policies == expected_scope_policies


def test_get_policies_for_resource_for_non_existing_index():
    """ Testing get_policies_for_resource
        for non existing index 'not_index'.
    """

    cluster = False
    indices = ['not_index']
    scope_policies = get_policies_for_resource(
        cluster, indices, SAMPLE_POLICIES
    )

    expected_scope_policies = []

    assert scope_policies == expected_scope_policies


def test_get_policies_for_resource_for_cluster():
    """ Testing get_policies_for_resource
        for cluster = True'.
    """

    cluster = True
    indices = []
    scope_policies = get_policies_for_resource(
        cluster, indices, SAMPLE_POLICIES
    )

    expected_scope_policies = [
        {
            'permissions': ['kibana_admin'],
            'scope': {'cluster': True},
            'users': ['alan']
        }
    ]

    assert scope_policies == expected_scope_policies


def test_get_policies_for_resource_for_all_indices():
    """ Testing get_policies_for_resource
        for indices = ['*'].
    """
    cluster = False
    indices = ['*', ]
    scope_policies = get_policies_for_resource(
        cluster, indices, SAMPLE_POLICIES
    )

    expected_scope_policies = [
        {
            'scope': {'indices': ['*']},
            'users': ['auditor'],
            'permissions': ['index_read']
        }
    ]

    assert scope_policies == expected_scope_policies
