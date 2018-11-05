from dockers import Docker
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

        self.create_phase()
        self.endFlag = False
        self.testLen = 30
        self.message = b'NULL'
        project = config.CONFIG['project']
        subscription_name_upstream = config.CONFIG['subscription_name_upstream']
        self.subscriber_upstream = pubsub_v1.SubscriberClient()
        self.subscription_path_upstream = self.subscriber_upstream.subscription_path(project, subscription_name_upstream)
        self.subscriber_upstream.subscribe(self.subscription_path_upstream, callback=self.callback)

        topic_name_downstream = config.CONFIG['topic_name_downstream']
        self.publisher_downstream = pubsub_v1.PublisherClient()
        self.topic_path_downstream = self.publisher_downstream.topic_path(project, topic_name_downstream)

        self.agents = 0
        self.messages = []

    def tearDown(self):
        self.send('END')

    def callback(self, message):
        if self.phase != message.attributes['phase']:
            return
        logging.info(message)
        self.messages.append(message.data.decode("utf-8"))
        message.ack()

    def create_phase(self, phase = ""):
        self.phase = 'phase_' + str(phase) + '_' + str(calendar.timegm(time.gmtime()))
        return self.phase

    def send(self, data):
        logging.info(data)
        data = data.encode('utf-8')
        self.publisher_downstream.publish(self.topic_path_downstream, data=data, phase=self.phase)

    def wait_for_response(self, num_messages = 1):
        for i in range(0, self.testLen):
            logging.info(len(self.messages))
            logging.info(self.messages)
            if len(self.messages) == num_messages:
                logging.info(self.messages)
                break
            time.sleep(1)

    def send_and_wait(self, data, phase=None):
        self.send(data)
        self.wait_for_response()

    def start_node_agent_pair(self, seeders=config.CONFIG['no_seeders']):
        docker = Docker()
        docker.stop('agent_' + str(self.agents))
        cmd = 'docker run --network=devnet --name agent_' + str(self.agents) + ' -v /root/spacemesh/devnet/tests:/opt/devnet -v /root/spacemesh/devnet/logs' + str(self.agents) + ':/opt/logs -v /root/spacemesh/devnet/cnf' + str(self.agents) + ':/opt/cnf/ -e SUBSCRIPTION_NAME_DOWNSTREAM=devnet_tests_agent_' + str(self.agents) + ' -e PHASE=' + self.phase + ' -e NODE=' + str(self.agents) + ' -e SEEDERS=' + seeders + ' spacemesh/devnet_agent:latest python3 /opt/devnet/base_test_agent.py'
        docker.start(cmd)
        self.agents += 1

if __name__ == '__main__':
    unittest.main()