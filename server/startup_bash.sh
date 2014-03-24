#!/bin/bash
python /home/docker/code/server/save_env.py

LOCAL_SETTINGS_FILE=/home/docker/code/globallometree/settings_local.py

cd /home/docker/code/es_proxy

echo ""
echo "Elasticsearch Proxy server"
echo ""
echo "Example command: python run_proxy.py"
echo ""

/bin/bash

echo "Hasta la vista" 