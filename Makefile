ES_PROXY_TAG_NAME ?= xela7/hatpull-elasticsearch-proxy
ES_PROXY_CONTAINER_NAME ?= tornado-elasticsearch-proxy

ES_PROXY_BASE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
ES_PROXY_BASE_DIR := $(abspath $(patsubst %/,%,$(dir $(ES_PROXY_BASE_PATH))))

ES_PROXY_PORT ?= 9225

ES_PROXY_OPTS  = --link ${ELASTIC_CONTAINER_NAME}:ES
ES_PROXY_OPTS += -e ES_PROXY_LISTEN_PORT=${ES_PROXY_PORT}
ES_PROXY_OPTS += -p ${ES_PROXY_PORT}:9225

#Useful for local debugging but not for actual run
ES_PROXY_DEBUG_OPTS = -v ${ES_PROXY_BASE_DIR}:/opt/code

#All commands should be prefixed with es-proxy
es-proxy-build:
	cd ${ES_PROXY_BASE_DIR} && docker build -t ${ES_PROXY_TAG_NAME} .

es-proxy-clean: stop
	-@docker rm ${ES_PROXY_CONTAINER_NAME} 2>/dev/null || true

es-proxy-stop:
	-@docker stop ${ES_PROXY_CONTAINER_NAME} 2>/dev/null || true

es-proxy-stop-bash:
	-@docker stop docker_es_proxy_bash 2>/dev/null || true

es-proxy-clean-bash: es-proxy-stop-bash
	-@docker rm docker_es_proxy_bash 2>/dev/null || true

es-proxy-run: es-proxy-clean
	docker run -d ${ES_PROXY_OPTS} --name ${ES_PROXY_CONTAINER_NAME} ${ES_PROXY_TAG_NAME} bash /opt/code/server/startup.sh

###################################### DEBUG ################################

es-proxy-run-bash: es-proxy-stop 
	docker run -i -t --rm ${ES_PROXY_OPTS} ${ES_PROXY_DEBUG_OPTS} ${ES_PROXY_TAG_NAME} bash /opt/code/server/startup_bash.sh
