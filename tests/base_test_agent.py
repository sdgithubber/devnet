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
        logging.basicConfig(format='%(asctime)s %(message)s')
        Logger.setLevel(logging.DEBUG)
        self.endFlag = False
    
        project = config.CONFIG['project']
        topic_name_upstream = config.CONFIG['topic_name_upstream']
        self.publisher_upstream = pubsub_v1.PublisherClient()
        self.topic_path_upstream = self.publisher_upstream.topic_path(project, topic_name_upstream)

        self.node = os.environ['NODE']
        self.docker = Docker()
        self.docker.stop('node_' + self.node)
        logging.debug('seeders:' + os.environ['SEEDERS'])
        self.modify_seeders(os.environ['SEEDERS'])
        self.phase = os.environ['PHASE']
        self.docker.start('docker run --network=devnet --name node_' + self.node + ' -p ' + str(7513 + int(self.node)) + ':7513 -v /root/spacemesh/devnet/logs' + self.node + ':/root/.spacemesh/nodes/ -v /root/spacemesh/devnet/tests/test.config.toml:/go/test.config.toml spacemesh/node:latest /go/src/github.com/spacemeshos/go-spacemesh/go-spacemesh -config /go/test.config.toml')
        subscription_name_downstream = os.environ['SUBSCRIPTION_NAME_DOWNSTREAM']
        self.subscriber_downstream = pubsub_v1.SubscriberClient()
        self.subscription_path_downstream = self.subscriber_downstream.subscription_path(project, subscription_name_downstream)
        time.sleep(5)

    def modify_seeders(self, seeders):
        file_name = "/opt/devnet/test.config.toml"

        with open(file_name) as f:
            new_config = f.read().replace('BOOT_NODES', 'bootnodes = ' + seeders)

        with open(file_name, "w") as f:
            f.write(new_config)

    def callback(self, message):
        logging.debug(message)
        self.message = message.data
        message.ack()
        logging.debug(message.attributes['phase'])
        if self.phase != message.attributes['phase']:
            logging.debug("NO_MESSAGE")
            return
        logging.debug(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " GOT_DOWN_MSG " + "".join(map(chr, self.message)))

        if b'END' == self.message:
            self.docker.stop('node_' + self.node)
            self.endFlag = True
        elif b'SEND_UP' == self.message:
            self.send('UP')
        elif b'GET_NODE_ID' == self.message:
            self.send(self.get_node_id())
        elif b'SHUTDOWN_NODE' == self.message:
            self.docker.stop('node_' + self.node)

    def act_on_request(self):
        self.subscriber_downstream.subscribe(self.subscription_path_downstream, callback=self.callback)
        while not self.endFlag:
            time.sleep(1)

    def send(self, data):
        data = data.encode('utf-8')
        self.publisher_upstream.publish(self.topic_path_upstream, data=data, phase=self.phase)

    def get_node_id(self):
        time.sleep(15)
        try:
            node_id = next(os.walk('/opt/logs'))[1][0]
        except Exception as e:
            logging.warning('Error finding log folder')
            logging.warning(e.__doc__ )
            return 'NULL'

        logging.debug('NodeId:' + node_id)
        return 'node_' + self.node + ':7513/' + node_id

if __name__ == '__main__':
    t = BaseDevnetAgent()
    t.act_on_request()