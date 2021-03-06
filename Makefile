# Makefile for Docker Landings

ifeq ($(findstring "/usr/lib/google-cloud-sdk/bin/:",PATH),"/usr/lib/google-cloud-sdk/bin/:")
	echo 1
	PATH="/usr/lib/google-cloud-sdk/bin/:${PATH}"
endif


help:
	@echo ""
	@echo "usage: make COMMAND"
	@echo ""
	@echo "Commands:"
	@echo "  install             Install enviroment and docker"
	@echo "  pull                Run git pull"
	@echo "  clean               Clean web folder and data"
	@echo "  build               Build Dockerfiles"
	@echo "  up                  Create and start containers"
	@echo "  down                Stop and clear all services"
	@echo "  logs                Follow log output"

install:
	@apt update
	@apt install curl software-properties-common apt-transport-https -y
	@curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	@add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(shell lsb_release -cs) stable"
	@apt update
	@apt install docker-ce -y
	@make build

clean_containers:
	@docker stop test_server 2>/dev/null || true

run:
	@mkdir -p $(shell pwd)/logs
	@rm -rf $(shell pwd)/logs/*.log
	@make clean_containers
	@if [ ! "$(sudo docker network ls | grep devnet)" ]; then sudo docker network create devnet || true; fi
	@docker run --rm --network=devnet --name test_server -e PUBSUB_VERIFICATION_TOKEN='1234' -e PUBSUB_TOPIC='topic' -e GOOGLE_CLOUD_PROJECT='spacemesh-198810' -v $(shell pwd)/tests:/opt/devnet spacemesh/devnet_agent:latest python3 /opt/devnet/tests.py >> $(shell pwd)/logs/test.log 2>&1 &

build:
	@gcloud auth configure-docker
	@make build_agent
	@make build_agent_packed
	@make build_node

build_agent:
	@docker build -f $(shell pwd)/agent/Dockerfile -t spacemesh/devnet_agent:latest .
	@docker tag spacemesh/node gcr.io/spacemesh-198810/node
	@docker push gcr.io/spacemesh-198810/devnet_agent

build_agent_packed:
	@docker build -f $(shell pwd)/agent/Dockerfile.code -t spacemesh/devnet_agent_packed:latest .
	@docker tag spacemesh/devnet_agent_packed gcr.io/spacemesh-198810/devnet_agent_packed
	@docker push gcr.io/spacemesh-198810/devnet_agent_packed

build_node:
	@wget https://raw.githubusercontent.com/spacemeshos/go-spacemesh/$(NODE)/Dockerfile -O Dockerfile.spacemesh.node
	@docker build -f $(shell pwd)/Dockerfile.spacemesh.node --build-arg BRANCH=$(NODE) -t spacemesh/node:latest .
	@docker tag spacemesh/devnet_agent gcr.io/spacemesh-198810/devnet_agent
	@docker push gcr.io/spacemesh-198810/node