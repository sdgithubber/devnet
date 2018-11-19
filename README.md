# devnet

Spacemesh's testing infrastructure. Answers all the testing needs of the spacemesh node.

## `Bootstrap`

Our first test scenario is to bootstrap a p2p network.

The following documentation assumes no prior knowledge on the setup and also should assume that all entities in the environment are blank. 

## Setting up an environment 
How to setup the environment
1. [Create a new ubuntu VM using GCP](https://cloud.google.com/compute/docs/instances/create-start-instance)
1. Connect the created machine using `sudo docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud compute --project "spacemesh-198810" ssh --zone "us-east4-c" "devnet-test-2"` where us-east4-c is the zone you created the the VM and the devnet-test-2 is the machine name you selected for.

`WARNING: The public SSH key file for gcloud does not exist.
WARNING: The private SSH key file for gcloud does not exist.
WARNING: You do not have an SSH key for gcloud.
WARNING: SSH keygen will be executed to generate a key.
This tool needs to create the directory [/root/.ssh] before being able
 to generate SSH keys.

Do you want to continue (Y/n)?
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/google_compute_engine.
Your public key has been saved in /root/.ssh/google_compute_engine.pub.
The key fingerprint is:
ba:53:6d:91:50:74:bd:1c:1b:be:15:db:e1:4f:c0:83 root@dd75a4122c38
The key's randomart image is:
+---[RSA 2048]----+
|         oo .+   |
|        .  .E Bo |
|         . . o.B=|
|          o   =o+|
|        S. .   +.|
|       .. o   . .|
|      .. .       |
|      ..         |
|      ..         |
+-----------------+
Updating project ssh metadata.../Updated [https://www.googleapis.com/compute/v1/projects/spacemesh-198810].
Updating project ssh metadata...done.
Waiting for SSH key to propagate.
Warning: Permanently added 'compute.5849460750300262232' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 16.04.5 LTS (GNU/Linux 4.15.0-1021-gcp x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

34 packages can be updated.
0 updates are security updates.


*** System restart required ***
Last login: Wed Nov 14 22:42:16 2018 from 52.202.226.187
root@devnet-test-2:~#`

1. Create a local user on the machine: `sudo useradd test`
1. Set password `sudo passwd test`
1. Add the user to the docker group `sudo usermod -aG docker test`
1. Install make `apt install make`

Installation and configuration
1. Create a new folder `mkdir -p /root/spacemesh/ && /root/spacemesh/`
1. Clone the project: `git clone https://github.com/spacemeshos/devnet.git && cd devnet`
```Cloning into 'devnet'...
remote: Enumerating objects: 102, done.
remote: Counting objects: 100% (102/102), done.
remote: Compressing objects: 100% (68/68), done.
remote: Total 1713 (delta 68), reused 63 (delta 34), pack-reused 1611
Receiving objects: 100% (1713/1713), 162.36 KiB | 0 bytes/s, done.
Resolving deltas: 100% (1200/1200), done.
Checking connectivity... done.```

1. Update the project configuration that can be found in tests/config.py to use the correct GCP project name, host, created user and password to the machine
`CONFIG = {
    'project': 'spacemesh-198810',
    'host': 'HOST_IP',
    'host_user': 'test',
    'host_password': 'PASSWORD',
    'no_seeders': '["0.0.0.0:7517/j7qWfWaJRVp25ZsnCu9rJ4PmhigZBtesB4YmQHqqPvtR"]',
    'node_port': 7513,
    'dht_timeout': 60
}`
1. Configure gcloud auth: `export PATH=/usr/lib/google-cloud-sdk/bin/:$PATH && gcloud auth configure-docker`
1. Update the project and build it using the relevant node branch: `git pull && NODE=hackathon make build`
`Already up-to-date.
gcloud credential helpers already registered correctly.
make[1]: Entering directory '/root/spacemesh/devnet'
Sending build context to Docker daemon  293.4kB
Step 1/10 : FROM ubuntu:16.04
 ---> b9e15a5d1e1a
Step 2/10 : RUN apt-get -y update && apt-get install -y python3 python3-pip
 ---> Using cache
 ---> 1ecefc6de9a0
Step 3/10 : RUN pip3 install --upgrade pip
 ---> Using cache
 ---> 7f3db3d9c17c
Step 4/10 : RUN pip3 install google-cloud google-cloud-pubsub spur
 ---> Using cache
 ---> e4eafc06c9ce
Step 5/10 : RUN mkdir -p /opt/devnet
 ---> Using cache
 ---> 34b8c01a566c
Step 6/10 : RUN mkdir -p /opt/cnf
 ---> Using cache
 ---> fbbbad2d39e9
Step 7/10 : RUN mkdir -p /opt/basecnf
 ---> Using cache
 ---> dd15b85b387b
Step 8/10 : RUN mkdir -p /opt/logs
 ---> Using cache
 ---> efdd9a65b425
Step 9/10 : ADD ./tests/test.config.toml /opt/basecnf/
 ---> Using cache
 ---> b507389fc260
Step 10/10 : WORKDIR /opt/devnet
 ---> Using cache
 ---> 37b6d1fbf61b
Successfully built 37b6d1fbf61b
Successfully tagged spacemesh/devnet_agent:latest
The push refers to repository [gcr.io/spacemesh-198810/devnet_agent]
6c9f3d75e904: Layer already exists
f1feb79fa705: Layer already exists
5bf37ec540e2: Layer already exists
c91b40f1248f: Layer already exists
ea97f7535ed5: Layer already exists
98df6609483a: Layer already exists
b106ac29b72d: Layer already exists
22e82de6079c: Layer already exists
75b79e19929c: Layer already exists
4775b2f378bb: Layer already exists
883eafdbe580: Layer already exists
19d043c86cbc: Layer already exists
8823818c4748: Layer already exists
latest: digest: sha256:a9ea81ce3bf30d6a12028bbf607c267d34362cada3847a1315efff3c4f22acb2 size: 3028
make[1]: Leaving directory '/root/spacemesh/devnet'
make[1]: Entering directory '/root/spacemesh/devnet'
Sending build context to Docker daemon  293.4kB
Step 1/2 : FROM gcr.io/spacemesh-198810/devnet_agent
 ---> 37b6d1fbf61b
Step 2/2 : ADD ./tests /opt/devnet
 ---> 11c7d9a5ed05
Successfully built 11c7d9a5ed05
Successfully tagged spacemesh/devnet_agent_packed:latest
The push refers to repository [gcr.io/spacemesh-198810/devnet_agent_packed]
226d5ea16fd5: Pushed
6c9f3d75e904: Layer already exists
f1feb79fa705: Layer already exists
5bf37ec540e2: Layer already exists
c91b40f1248f: Layer already exists
ea97f7535ed5: Layer already exists
98df6609483a: Layer already exists
b106ac29b72d: Layer already exists
22e82de6079c: Layer already exists
75b79e19929c: Layer already exists
4775b2f378bb: Layer already exists
883eafdbe580: Layer already exists
19d043c86cbc: Layer already exists
8823818c4748: Layer already exists
latest: digest: sha256:1d7ee2292fcf008cbd1af651da3e927b7c4c2ec1275a36bfd792f718a8e90550 size: 3236
make[1]: Leaving directory '/root/spacemesh/devnet'
make[1]: Entering directory '/root/spacemesh/devnet'
--2018-11-19 10:53:39--  https://raw.githubusercontent.com/spacemeshos/go-spacemesh/hackathon/Dockerfile
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.64.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 741 [text/plain]
Saving to: ‘Dockerfile.spacemesh.node’

Dockerfile.spacemesh.node                 100%[=====================================================================================>]     741  --.-KB/s    in 0s

2018-11-19 10:53:39 (140 MB/s) - ‘Dockerfile.spacemesh.node’ saved [741/741]

Sending build context to Docker daemon  294.9kB
Step 1/14 : FROM golang:1.9.2-alpine3.6 AS build
 ---> bbab7aea1231
Step 2/14 : ARG BRANCH=hackathon
 ---> Using cache
 ---> 2eb4b66121ee
Step 3/14 : RUN apk add --no-cache make git
 ---> Using cache
 ---> f73fdbdf7f0b
Step 4/14 : RUN go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
 ---> Using cache
 ---> 1e179f05228e
Step 5/14 : RUN go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
 ---> Using cache
 ---> 4ca313b46192
Step 6/14 : RUN go get -u github.com/golang/protobuf/protoc-gen-go
 ---> Using cache
 ---> 52e9a6020d37
Step 7/14 : RUN go get -u github.com/kardianos/govendor
 ---> Using cache
 ---> 840eda524d42
Step 8/14 : RUN echo ${BRANCH}
 ---> Using cache
 ---> c6d0d55e0061
Step 9/14 : RUN mkdir -p src/github.com/spacemeshos; cd src/github.com/spacemeshos; git clone https://github.com/spacemeshos/go-spacemesh; cd go-spacemesh; git checkout ${BRANCH}; go build; govendor sync; make
 ---> Using cache
 ---> dcba938f6360
Step 10/14 : RUN cp /go/src/github.com/spacemeshos/go-spacemesh/config.toml /go
 ---> Using cache
 ---> b21b1906d916
Step 11/14 : ENTRYPOINT /go/src/github.com/spacemeshos/go-spacemesh/go-spacemesh $BOOTPARAMS
 ---> Using cache
 ---> 70e743ffc671
Step 12/14 : EXPOSE 7513
 ---> Using cache
 ---> adb419b8a546
Step 13/14 : EXPOSE 9090
 ---> Using cache
 ---> e33f8fcdb306
Step 14/14 : EXPOSE 9091
 ---> Using cache
 ---> 42382cc3e62a
Successfully built 42382cc3e62a
Successfully tagged spacemesh/node:latest
The push refers to repository [gcr.io/spacemesh-198810/node]
0d1f12be232f: Layer already exists
6fa759e67ae3: Layer already exists
6825081aefdc: Layer already exists
0a2074c6a213: Layer already exists
5e593dd13500: Layer already exists
8f0d2fb41089: Layer already exists
d5f9cd047948: Layer already exists
ae5b46d58acc: Layer already exists
c822f55f6bee: Layer already exists
d7bb0a15da32: Layer already exists
ff6f438bec54: Layer already exists
d8e80354a27b: Layer already exists
9dfa40a0da3b: Layer already exists
latest: digest: sha256:312dbd87cf89b32ac6c57d3ebcd8cac6da04d07f0fa4ff88dc253bb62532449d size: 3049
make[1]: Leaving directory '/root/spacemesh/devnet'`

## Running the implemented tests on devnet
All tests are encapsulated in a single file name tests.py
1. Run the tests: `make run`
`make[1]: Entering directory '/root/spacemesh/devnet'
make[1]: Leaving directory '/root/spacemesh/devnet'
Error response from daemon: network with name devnet already exists`
What to expect as a result
1. Results can be find the tests output file: more 
1. The bottom of the file includes the number of tests that were run and OK if everything is okay or errors if the tests failed
`.
----------------------------------------------------------------------
Ran 3 tests in 111.561s

OK`