#!/bin/bash
python /opt/code/server/save_env.py
pip install -vr /opt/code/server/requirements.txt

cd /opt/code/es_proxy

echo 
echo "Elasticsearch Proxy Server"
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