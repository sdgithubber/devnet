FROM ubuntu:16.04

RUN apt-get -y update && apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install flask google-cloud google-cloud-pubsub
RUN mkdir /opt/devnet
WORKDIR /opt/devnet