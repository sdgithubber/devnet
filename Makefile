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

run:
	@rm -rf $(shell pwd)/test.log
	@if [ ! "$(sudo docker network ls | grep devnet)" ]; then sudo docker network create devnet || true; fi
	@(docker stop agent && docker rm agent) || echo "" &&\
	docker run --network=devnet --name agent -p 8080:8080 -e PUBSUB_VERIFICATION_TOKEN='1234' -e PUBSUB_TOPIC='topic' -e GOOGLE_CLOUD_PROJECT='spacemesh-198810' -v $(shell pwd)/tests:/opt/devnet spacemesh/devnet_agent:latest python3 /opt/devnet/base_test_agent.py  >> $(shell pwd)/test.log 2>&1 &
	@(docker stop node && docker rm node) || echo "" &&\
	docker run --network=devnet --name node -p 7513:7513 /go/src/github.com/spacemeshos/go-spacemesh/go-spacemesh >> $(shell pwd)/node.log 2>&1 &
	@(docker stop test_server && docker rm test_server) || echo "" &&\
	docker run --network=devnet --name test_server -e PUBSUB_VERIFICATION_TOKEN='1234' -e PUBSUB_TOPIC='topic' -e GOOGLE_CLOUD_PROJECT='spacemesh-198810' -v $(shell pwd)/tests:/opt/devnet spacemesh/devnet_agent:latest python3 /opt/devnet/tests.py >> $(shell pwd)/test.log 2>&1 &

build:
	@docker build -f $(shell pwd)/agent/Dockerfile -t spacemesh/devnet_agent:latest .
	@wget https://github.com/spacemeshos/go-spacemesh/blob/develop/Dockerfile -O Dockerfile.spacemesh.node
	@docker build -f $(shell pwd)/agent/Dockerfile.spacemesh.node -t spacemesh/node:latest .