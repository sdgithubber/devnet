import config
from dockers import Docker
from topics import Publisher, Subscriber
from google.cloud import pubsub_v1
import time
import datetime
from subprocess import call
import os
import re
import logging
from logging import Logger

class BaseDevnetAgent:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
        self.endFlag = False

        self.dht_timeout = config.CONFIG['dht_timeout']
        self.node_id = "NULL"
        self.node = os.environ['NODE']
        self.phase = os.environ['PHASE']
        self.node_port = config.CONFIG['node_port']
        self.docker = Docker()
        self.start_node()
        self.establish_links()

    def establish_links(self):
        self.project = config.CONFIG['project']
        self.down_subscriber = Subscriber(self.project, os.environ['SUBSCRIPTION_NAME_DOWNSTREAM'])
        self.down_subscriber.subscribe(self.callback)
        self.up_publisher = Publisher(self.project, os.environ['TOPIC_PATH_UPSTREAM'])

    def start_node(self):
        logging.info('seeders:' + os.environ['SEEDERS'])
        self.modify_seeders(os.environ['SEEDERS'], os.environ['BOOTSTRAP'], os.environ['RANDCON'])
        self.docker.stop('node_' + self.node)
        self.docker.start('docker run --network=devnet --name node_' + self.node + ' -p ' + str(self.node_port + int(self.node)) + ':' + str(self.node_port) + ' -v /root/spacemesh/devnet/logs' + self.node + ':/root/.spacemesh/nodes/ -v /root/spacemesh/devnet/cnf' + self.node + '/test.config.toml:/root/config.toml spacemesh/node:latest /go/src/github.com/spacemeshos/go-spacemesh/go-spacemesh --config=/root/config.toml > /root/spacemesh/devnet/logs' + self.node + '/node.log')

        while self.get_node_id() == 'NULL':
            time.sleep(1)

    def modify_seeders(self, seeders, bootstrap, randcon):
        file_name = "/opt/basecnf/test.config.toml"
        out_file_name = "/opt/cnf/test.config.toml"

        with open(file_name) as f:
            new_config = f.read().replace('BOOT_NODES', 'bootnodes = ' + seeders[1:-1]).replace('BOOTSTRAP_VALUE', bootstrap).replace('RANDCON', randcon)

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
            self.down_subscriber.delete()
            self.endFlag = True
        elif 'SEND_UP' == self.message:
            self.send('UP')
        elif 'GET_NODE_ID' == self.message:
            self.send(self.get_node_id())
        elif 'GET_DHT_SIZE' == self.message:
            self.send(str(self.get_dht_size()))
        elif 'SHUTDOWN_NODE' == self.message:
            self.docker.stop('node_' + self.node)

    def act_on_request(self):
        while not self.endFlag:
            time.sleep(1)

    def send(self, data):
        logging.info("sent: " + str(data))
        data = data.encode('utf-8')
        self.up_publisher.publish(data=data, phase=self.phase)

    def get_node_id(self):
        try:
            self.node_id = next(os.walk('/opt/logs'))[1][0]
        except Exception as e:
            logging.warning('Error finding log folder')
            logging.warning(e.__doc__ )
            return 'NULL'

        logging.info('NodeId:' + self.node_id)
        return 'node_' + self.node + ':' + str(self.node_port) + '/' + self.node_id

    def get_dht_size(self):
        pattern = re.compile(u'.*DHT Bootstrapped with (\d+)')
        for i in range(0, self.dht_timeout):
            for line in open('/opt/logs/' + self.node_id + '/node.log', "r", encoding="utf-8"):
                results = pattern.match(line)
                if results != None:
                    return results.group(1)
            time.sleep(1)
        return 0

if __name__ == '__main__':
    t = BaseDevnetAgent()
    t.act_on_request()