from ..functions import get_available_policies_for_resource

from .constants import SAMPLE_POLICIES


def test_get_available_policies_for_resource_for_index_kibana_int():
    """ For index kibana-int. """
    cluster = False
    indices = ['kibana-int']
    scope_policies = get_available_policies_for_resource(
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


def test_get_available_policies_for_resource_for_non_existing_index():
    """ Testing get_available_policies_for_resource
        for non existing index 'not_index'.
    """

    cluster = False
    indices = ['not_index']
    scope_policies = get_available_policies_for_resource(
        cluster, indices, SAMPLE_POLICIES
    )

    expected_scope_policies = []

    assert scope_policies == expected_scope_policies


def test_get_available_policies_for_resource_for_cluster():
    """ Testing get_available_policies_for_resource
        for cluster = True'.
    """

    cluster = True
    indices = []
    scope_policies = get_available_policies_for_resource(
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