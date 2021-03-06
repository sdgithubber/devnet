from dockers import Docker
from topics import Publisher, Subscriber
import config
import os
import time
import calendar
from google.cloud import pubsub_v1
import unittest
import spur
import logging
from logging import Logger

class BaseTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

        self.nodes_list = []
        self.phases = []
        self.endFlag = False
        self.testLen = 60
        self.message = b'NULL'

        self.project = config.CONFIG['project']
        self.up_publisher = Publisher(self.project)
        self.up_topic_path = self.up_publisher.create()
        self.up_publisher.add_subscription().subscribe(self.callback)
        self.down_publisher = Publisher(self.project)
        self.down_publisher.create()

        self.agents = 0
        self.messages = []

    def tearDown(self):
        for self.phase in self.phases:
            self.send('END')
        self.up_publisher.delete()
        self.down_publisher.delete()

    def callback(self, message):
        if self.phase != message.attributes['phase']:
            return
        logging.info(message)
        self.messages.append(message.data.decode("utf-8"))
        message.ack()

    def create_phase(self, phase = ""):
        self.phase = 'phase_' + str(phase) + '_' + str(calendar.timegm(time.gmtime()))
        self.phases.append(self.phase)
        return self.phase

    def send(self, data):
        self.messages = []
        logging.info(data)
        data = data.encode('utf-8')
        self.down_publisher.publish(data=data, phase=self.phase)

    def wait_for_response(self, num_messages = 1):
        for i in range(0, self.testLen):
            if len(self.messages) == num_messages:
                logging.info(self.messages)
                break
            time.sleep(1)

    def send_and_wait(self, data, nodes):
        self.send(data)
        self.wait_for_response(nodes)
        self.assertEqual(nodes, len(self.messages))
        return self.messages

    def start_node_agent_pair(self, seeders=config.CONFIG['no_seeders'], bootstrap = 'false', randcon = 5):
        docker = Docker()
        docker.stop('agent_' + str(self.agents))
        down_subscriber = self.down_publisher.add_subscription()
        cmd = 'docker run --network=devnet --name agent_' + str(self.agents) + ' -v /root/spacemesh/devnet/tests:/opt/devnet -v /root/spacemesh/devnet/logs' + str(self.agents) + ':/opt/logs -v /root/spacemesh/devnet/cnf' + str(self.agents) + ':/opt/cnf/ -e SUBSCRIPTION_PATH_DOWNSTREAM=' + down_subscriber.subscription_path + ' -e TOPIC_PATH_UPSTREAM=' + self.up_topic_path + ' -e PHASE=' + self.phase + ' -e BOOTSTRAP=' + bootstrap +' -e NODE=' + str(self.agents) + ' -e SEEDERS=' + seeders + ' -e RANDCON=' + str(randcon) + ' spacemesh/devnet_agent:latest python3 /opt/devnet/base_test_agent.py'
        docker.start(cmd)
        self.agents += 1

    def run_phase(self, nodes = 1, seeders=config.CONFIG['no_seeders'], bootstrap = 'false', randcon = 5, message = ''):
        self.create_phase(len(self.phases))
        for i in range(0, nodes):
            self.start_node_agent_pair(seeders = seeders, bootstrap = bootstrap, randcon = randcon)
        self.send_and_wait('GET_NODE_ID', nodes)
        self.nodes_list += self.messages
        return self.messages

if __name__ == '__main__':
    unittest.main()