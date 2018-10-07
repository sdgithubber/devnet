# Makefile for Docker Landings

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
	@docker stop agent 2>/dev/null || true
	@docker stop node 2>/dev/null || true
	@docker stop cleaner 2>/dev/null || true
	@docker stop test_server 2>/dev/null || true

run:
	@mkdir -p $(shell pwd)/logs
	@rm -rf $(shell pwd)/logs/*.log
	@make clean_containers
	@if [ ! "$(sudo docker network ls | grep devnet)" ]; then sudo docker network create devnet || true; fi
	@docker run --rm --network=devnet --name node -p 7513:7513 spacemesh/node:latest /go/src/github.com/spacemeshos/go-spacemesh/go-spacemesh >> $(shell pwd)/logs/node.log 2>&1 &
	@docker run --rm --network=devnet --name cleaner -e PUBSUB_VERIFICATION_TOKEN='1234' -e PUBSUB_TOPIC='topic' -e GOOGLE_CLOUD_PROJECT='spacemesh-198810' -v $(shell pwd)/tests:/opt/devnet spacemesh/devnet_agent:latest python3 /opt/devnet/base_cleaner.py >> $(shell pwd)/logs/cleaner.log 2>&1
	@docker run --rm --network=devnet --name agent -p 8080:8080 -e PUBSUB_VERIFICATION_TOKEN='1234' -e PUBSUB_TOPIC='topic' -e GOOGLE_CLOUD_PROJECT='spacemesh-198810' -v $(shell pwd)/tests:/opt/devnet -v $(shell pwd)/logs:/opt/logs spacemesh/devnet_agent:latest python3 /opt/devnet/base_test_agent.py >> $(shell pwd)/logs/test.log 2>&1 &
	@docker run --rm --network=devnet --name test_server -e PUBSUB_VERIFICATION_TOKEN='1234' -e PUBSUB_TOPIC='topic' -e GOOGLE_CLOUD_PROJECT='spacemesh-198810' -v $(shell pwd)/tests:/opt/devnet spacemesh/devnet_agent:latest python3 /opt/devnet/tests.py >> $(shell pwd)/logs/test.log 2>&1 &

build:
	@docker build -f $(shell pwd)/agent/Dockerfile -t spacemesh/devnet_agent:latest .
	@wget https://raw.githubusercontent.com/spacemeshos/go-spacemesh/develop/Dockerfile -O Dockerfile.spacemesh.node
	@docker build -f $(shell pwd)/Dockerfile.spacemesh.node -t spacemesh/node:latest .