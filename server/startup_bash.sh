#!/bin/bash
python /opt/code/server/save_env.py

cd /opt/code/es_proxy

echo 
echo "Elasticsearch Proxy"
echo 
echo
echo "Example command: python run_proxy.py"
echo "Then open http://localhost:${ES_PROXY_LISTEN_PORT} to try out the server"
echo
echo "Run tests"
echo "python tests.py"
echo
echo "Note: If you are using vagrant, port ${ES_PROXY_LISTEN_PORT} must also be forwarded in your Vagrantfile"
echo

/bin/bash

echo "Hasta la vista" 