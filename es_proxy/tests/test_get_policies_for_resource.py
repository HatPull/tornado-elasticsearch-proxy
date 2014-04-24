from ..functions import get_policies_for_resource

from .constants import SAMPLE_POLICIES


def test_get_policies_for_resource_for_index_kibana_int():
    """ For index kibana-int. """
    cluster = False
    indices = ['kibana-int']
    resource_policies = get_policies_for_resource(
        cluster, indices, SAMPLE_POLICIES
    )

    expected_resource_policies = [
        {
            'permissions': ['index_write', 'index_read'],
            'resources': {'indices': ['kibana-int']},
            'users': ['*']
        }
    ]

    assert resource_policies == expected_resource_policies


def test_get_policies_for_resource_with_bad_policy():
    """ Testing get_policies_for_resource
        with bad resources key.
    """

    BAD_POLICY = [
        {
            'resources': {'weird_key': ['*']},
            'users': ['*']
        }
    ]
    cluster = False
    indices = None
    resource_policies = get_policies_for_resource(
        cluster, indices, BAD_POLICY
    )

    expected_resource_policies = []

    assert resource_policies == expected_resource_policies


def test_get_policies_for_resource_for_non_existing_index():
    """ Testing get_policies_for_resource
        for non existing index 'not_index'.
    """

    cluster = False
    indices = ['not_index']
    resource_policies = get_policies_for_resource(
        cluster, indices, SAMPLE_POLICIES
    )

    expected_resource_policies = []

    assert resource_policies == expected_resource_policies


def test_get_policies_for_resource_for_cluster():
    """ Testing get_policies_for_resource
        for cluster = True'.
    """

    cluster = True
    indices = []
    resource_policies = get_policies_for_resource(
        cluster, indices, SAMPLE_POLICIES
    )

    expected_resource_policies = [
        {
            'permissions': ['kibana_admin'],
            'resources': {'cluster': True},
            'users': ['alan']
        }
    ]

    assert resource_policies == expected_resource_policies


def test_get_policies_for_resource_for_all_indices():
    """ Testing get_policies_for_resource
        for indices = ['*'].
    """
    cluster = False
    indices = ['*', ]
    resource_policies = get_policies_for_resource(
        cluster, indices, SAMPLE_POLICIES
    )

    expected_resource_policies = [
        {
            'resources': {'indices': ['*']},
            'users': ['auditor'],
            'permissions': ['index_read']
        }
    ]

    assert resource_policies == expected_resource_policies
