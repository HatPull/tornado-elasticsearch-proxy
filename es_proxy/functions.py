import re

import settings


script_regex = re.compile("script|script_fields[\"']+\s*:\s*\{")


def parse_request(request):
    """
        TODO:  Should this function be "parse_request_uri"  ?


        Parses a tornado http request object

        Returns a list of properties that define the request

        call / string /
            a string representing the type of call being made to elasticsearch
        cluster / boolean /
            does this request apply to the cluster resources?
        indices / list /
            a simple list of indices that are included in the request
        scripted / boolean /
            does this call include elasticsearch script?

        script example:
            http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/query-dsl-script-filter.html

    """

    parsed = {}

    # Figure out what the call is to elasticsearch
    # Cut the first slash "/" off the path and split the rest on forward slash
    path_parts = request.path[1:].split('/')

    # we are looking for calls which are not meta_calls.
    # if we find an underscored word, not in the meta_calls list,
    # it becomes the returned call.
    meta_calls = ['_all', '_primary', '_local']
    for part in path_parts:
        if part.startswith('_') and part not in meta_calls:
            parsed['call'] = part
            break

    # If a call (such as _search or _update) was not found,
    # we add the two calls _home, and _document
    # that don't exist in the real elasticsearch path.
    # assuming home if the path is empty or one char
    # and _document if the path is longer
    if 'call' not in parsed.keys():
        if request.path == '/':
            parsed['call'] = '_home'
        else:
            parsed['call'] = '_document'

    #Is this a cluster call, or a call to indices?
    if (
        request.path == '/' or
        path_parts[0].startswith('_') and
        path_parts[0] != '_all'
    ):
        #This is a call to the root or "cluster" so we set cluster to be true
        parsed['cluster'] = True
        parsed['indices'] = []
    else:
        #This is a call to an index or multiple indices - so we get those
        parsed['cluster'] = False
        parsed['indices'] = path_parts[0].split(',')

    if script_regex.search(request.body):
        parsed['scripted'] = True
    else:
        parsed['scripted'] = False
    return parsed


def get_policies_for_resource(cluster, indices, policies):
    """
    Find policies that apply to a given resource.

    cluster / boolean /
        does the policy apply to the root resources
        or calls that read about or affect the cluster
    indices / list /
        a simple list of index name that the policy applies to
    policies / list of dicts /
        A list of policies to check against the cluster and indices

    Returns: a list of policies that apply to the given resource.

    """
    resource_policies = []
    for policy in policies:
        if (
            'cluster' in policy['resources'].keys()
            and cluster
            and policy['resources']['cluster']
        ):
            resource_policies.append(policy)
        elif 'indices' in policy['resources'].keys():
            for index in indices:
                if index in policy['resources']['indices']:
                    resource_policies.append(policy)

    return resource_policies


def get_policies_for_user(user, policies):
    """
    Find policies that apply to a given user

    user / string /
        the name of the authenticated user
    policies / list of dicts /
        A list of policies to check against the cluster and indices

    Returns: a list of policies that apply to the given user

    """
    user_available_policies = []
    for policy in policies:
        if '*' in policy['users']:
            user_available_policies.append(policy)
        elif user in policy['users']:
            user_available_policies.append(policy)

    return user_available_policies


def authenticate_call_and_method(policies, call, method):
    """ Discover if call and method pair is found within policies.
    """
    for policy in policies:
        for permission_name in policy['permissions']:
            permission = settings.PERMISSIONS[permission_name]

            # Is the call authorized?
            call_authorized = \
                permission['calls'] == '*' or \
                call in permission['calls']

            # Is the method authorized?
            method_authorized = \
                permission['methods'] == '*' or \
                method in permission['methods']

            if call_authorized and method_authorized:
                print "USER:%s GRANTED WITH: %s" % (
                    policy['users'],
                    permission
                )
                return True
        return False
