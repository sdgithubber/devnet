import config
from dockers import Docker
from google.cloud import pubsub_v1
import time
import datetime
from subprocess import call
import os
import logging
from logging import Logger

class BaseDevnetAgent:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
        self.endFlag = False

        self.node = os.environ['NODE']
        self.phase = os.environ['PHASE']
        self.node_port = config.CONFIG['node_port']
        self.docker = Docker()
        self.start_node()
        self.establish_links()

    def establish_links(self):
        project = config.CONFIG['project']
        topic_name_upstream = config.CONFIG['topic_name_upstream']
        self.publisher_upstream = pubsub_v1.PublisherClient()
        self.topic_path_upstream = self.publisher_upstream.topic_path(project, topic_name_upstream)

        subscription_name_downstream = os.environ['SUBSCRIPTION_NAME_DOWNSTREAM']
        self.subscriber_downstream = pubsub_v1.SubscriberClient()
        self.subscription_path_downstream = self.subscriber_downstream.subscription_path(project, subscription_name_downstream)

    def start_node(self):
        logging.info('seeders:' + os.environ['SEEDERS'])
        self.modify_seeders(os.environ['SEEDERS'], os.environ['BOOTSTRAP'])
        self.docker.stop('node_' + self.node)
        self.docker.start('docker run --network=devnet --name node_' + self.node + ' -p ' + str(self.node_port + int(self.node)) + ':' + str(self.node_port) + ' -v /root/spacemesh/devnet/logs' + self.node + ':/root/.spacemesh/nodes/ -v /root/spacemesh/devnet/cnf' + self.node + '/test.config.toml:/root/config1.toml spacemesh/node:latest /go/src/github.com/spacemeshos/go-spacemesh/go-spacemesh --config=/root/config.toml')

        while self.get_node_id() == 'NULL':
            time.sleep(1)

    def modify_seeders(self, seeders, bootstrap):
        file_name = "/opt/basecnf/test.config.toml"
        out_file_name = "/opt/cnf/test.config.toml"

        with open(file_name) as f:
            new_config = f.read().replace('BOOT_NODES', 'bootnodes = ' + seeders[1:-1]).replace('BOOTSTRAP_VALUE', bootstrap)

        with open(out_file_name, "w") as f:
            f.write(new_config)

    def callback(self, message):
        logging.info(message)
        self.message = "".join(map(chr, message.data))
        message.ack()
        logging.info(message.attributes['phase'])
        if self.phase != message.attributes['phase']:
            logging.info("NO_MESSAGE")
            return
        logging.info("GOT_DOWN_MSG " + self.message)

        if 'END' == self.message:
            self.docker.stop('node_' + self.node)
            self.endFlag = True
        elif 'SEND_UP' == self.message:
            self.send('UP')
        elif 'GET_NODE_ID' == self.message:
            self.send(self.get_node_id())
        elif 'SHUTDOWN_NODE' == self.message:
            self.docker.stop('node_' + self.node)

    def act_on_request(self):
        self.subscriber_downstream.subscribe(self.subscription_path_downstream, callback=self.callback)
        while not self.endFlag:
            time.sleep(1)

    def send(self, data):
        logging.info("sent: " + data)
        data = data.encode('utf-8')
        self.publisher_upstream.publish(self.topic_path_upstream, data=data, phase=self.phase)

    def get_node_id(self):
        try:
            node_id = next(os.walk('/opt/logs'))[1][0]
        except Exception as e:
            logging.warning('Error finding log folder')
            logging.warning(e.__doc__ )
            return 'NULL'

        logging.info('NodeId:' + node_id)
        return 'node_' + self.node + ':' + str(self.node_port) + '/' + node_id

if __name__ == '__main__':
    t = BaseDevnetAgent()
    t.act_on_request()