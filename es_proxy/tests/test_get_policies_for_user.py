from .constants import SAMPLE_POLICIES
from ..functions import get_policies_for_user


def test_get_policies_for_user():
    """ Testing get_policies_for_user
    """
    user = 'alan'

    expected_user_policies = [
        {
            'permissions': ['index_write', 'index_read'],
            'resources': {'indices': ['kibana-int']},
            'users': ['*']
        },
        {
            'permissions': ['kibana_admin'],
            'resources': {'cluster': True},
            'users': ['alan']
        }
    ]

    user_policies = get_policies_for_user(
        user, SAMPLE_POLICIES
    )

    assert user_policies == expected_user_policies
