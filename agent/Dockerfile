FROM ubuntu:16.04

RUN apt-get -y update && apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install google-cloud google-cloud-pubsub spur
RUN mkdir -p /opt/devnet
RUN mkdir -p /opt/cnf/
RUN mkdir -p /opt/basecnf/
ADD ./tests/test.config.toml /opt/basecnf/
WORKDIR /opt/devnet