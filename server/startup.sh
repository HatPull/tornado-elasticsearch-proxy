#!/bin/bash
#Save the environment that was passed in
python /opt/code/server/save_env.py
#Run the proxy server
python /opt/code/es_proxy/run_proxy.py