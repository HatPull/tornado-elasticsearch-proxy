from .constants import SAMPLE_POLICIES
from ..functions import get_available_policies_for_user
# from pprint import pprint


# print "User: joe"
# #Test a few policies for users
# user = 'joe'
# user_policies = get_user_available_policies(user, SAMPLE_POLICIES)
# pprint(user_policies)
# print

# print "User: bob"
# #Test a few policies for users
# user = 'bob'
# user_policies = get_user_available_policies(user, SAMPLE_POLICIES)
# pprint(user_policies)
# print

def test_get_available_policies_for_user():
    """ Testing get_available_policies_for_user
    """
    user = 'alan'

    expected_user_policies = [
        {
            'permissions': ['index_write', 'index_read'],
            'scope': {'indices': ['kibana-int']},
            'users': ['*']
        },
        {
            'permissions': ['kibana_admin'],
            'scope': {'cluster': True},
            'users': ['alan']
        }
    ]

    user_policies = get_available_policies_for_user(
        user, SAMPLE_POLICIES
    )

    assert user_policies == expected_user_policies
