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
	@apt install curl -y
	@curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	@add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(shell lsb_release -cs) stable"
	@apt update
	@apt install docker-ce -y
	@make build

run:
	@docker run --network=worker_net --name agent -p 80:80 -v $(shell pwd)/tests:/opt/devnet spacemesh/devnet_agent:latest /opt/devnet/basic_test_agent.py  >> $(shell pwd)/test.log 2>&1 &
	@docker run --network=worker_net --name test_server -v $(shell pwd)/tests:/opt/devnet spacemesh/devnet_agent:latest /opt/devnet/basic_test_ci.py >> $(shell pwd)/test.log 2>&1 &

build:
	@docker build -f $(shell pwd)/agent/Dockerfile -t spacemesh/devnet_agent:latest .