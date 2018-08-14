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
	@make clean
	@make build

run:

clean:
	@rm -rf $(shell pwd)/web && mkdir web

build:
	@docker build -f $(shell pwd)/web/docker/Dockerfile.cron -t spacemesh/devnet_agent:latest .