
PROJECT_ROOT = $(shell pwd)

build:
	docker build -t docker_es_proxy_image github.com/HatPull/tornado-elasticsearch-proxy

build-local:
	docker build -t docker_es_proxy_image .

clean: stop
	-@docker rm docker_es_proxy 2>/dev/null || true

stop:
	-@docker stop docker_es_proxy 2>/dev/null || true


###################################### DEBUG ################################

run-bash: stop clean-bash
	docker run -i -t -name docker_es_proxy_bash -link elasticsearch_server:ES -p 9225:9225 -v ${PROJECT_ROOT}:/home/docker/code docker_es_proxy_image bash /home/docker/code/server/startup_bash.sh

stop-bash:
	-@docker stop docker_es_proxy_bash 2>/dev/null || true

clean-bash: stop-bash
	-@docker rm docker_es_proxy_bash 2>/dev/null || true

logs:
	docker logs docker_es_proxy