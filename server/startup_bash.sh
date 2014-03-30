#!/bin/bash
python /opt/code/server/save_env.py

LOCAL_SETTINGS_FILE=/opt/code/globallometree/settings_local.py

cd /opt/code/es_proxy

echo ""
echo "Elasticsearch Proxy server"
echo ""
echo "Example command: python run_proxy.py"
echo ""

/bin/bash

echo "Hasta la vista" 