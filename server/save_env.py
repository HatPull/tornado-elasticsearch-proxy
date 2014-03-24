import os
import json

env_safe_dict = {}
for k,v in os.environ.iteritems():
    if type(v) == str:
        env_safe_dict[k] = v

with open('/home/docker/env.json', 'w') as outfile:
    json.dump(env_safe_dict, outfile, indent=4, sort_keys=True)