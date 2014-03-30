
ES_PROXY_TAG_NAME ?= tomgruner/globallometree-elasticsearch-proxy
ES_PROXY_CONTAINER_NAME ?= tornado-elasticsearch-proxy

ES_PROXY_BASE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
ES_PROXY_BASE_DIR := $(abspath $(patsubst %/,%,$(dir $(ES_PROXY_BASE_PATH))))



#All commands should be prefixed with es-proxy
es-proxy-build:
	cd ${ES_PROXY_BASE_DIR} && docker build -t ${ES_PROXY_TAG_NAME} .

es-proxy-clean: stop
	-@docker rm ${ES_PROXY_CONTAINER_NAME} 2>/dev/null || true

es-proxy-stop:
	-@docker stop ${ES_PROXY_CONTAINER_NAME} 2>/dev/null || true

es-proxy-run:
	docker run -d ${ES_PROXY_CONTAINER_NAME} /opt/code/es_proxy/run_proxy.py


###################################### DEBUG ################################

es-proxy-run-bash: stop clean-bash
	docker run -i -t --name ${ES_PROXY_CONTAINER_NAME}_bash -link ${ELASTIC_CONTAINER_NAME}:ES -p 9225:9225 -v ${PROJECT_ROOT}:/opt/code docker_es_proxy_image bash /opt/code/server/startup_bash.sh

es-proxy-stop-bash:
	-@docker stop docker_es_proxy_bash 2>/dev/null || true

es-proxy-clean-bash: es-proxy-stop-bash
	-@docker rm docker_es_proxy_bash 2>/dev/null || true
