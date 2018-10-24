import config
import os
import time
from google.cloud import pubsub_v1
import unittest
import spur

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.endFlag = False
        self.testLen = 20
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

    def tearDown(self):
        self.send('END')

    def callback(self, message):
        self.message = message.data
        message.ack()
        self.endFlag = True

    def send(self, data):
        data = data.encode('utf-8')
        self.publisher_downstream.publish(self.topic_path_downstream, data=data)

    def wait_for_response(self):
        for i in range(0, self.testLen):
            if self.endFlag:
                print(self.message)
                break
            time.sleep(1)

    def send_and_wait(self, data):
        self.send(data)
        self.wait_for_response()

    def start_node_agent_pair(self):
        Docker.stop('node_' + str(self.agents))
        Docker.start('docker run --network=devnet --name node_' + str(self.agents) + ' -p ' + str(7513 + self.agents) + ':7513 -v /root/spacemesh/devnet/logs:/root/.spacemesh/nodes/ spacemesh/node:latest /go/src/github.com/spacemeshos/go-spacemesh/go-spacemesh')
        Dockers.stop('agent_' + str(self.agents))
        Dockers.start('docker run --network=devnet --name agent_' + str(self.agents) + ' -v /root/spacemesh/devnet/tests:/opt/devnet -v /root/spacemesh/devnet/logs:/opt/logs -e SUBSCRIPTION_NAME_DOWNSTREAM=devnet_tests_agent_' + str(self.agents) + ' -e NODE=node_' + str(self.agents) + ' spacemesh/devnet_agent:latest python3 /opt/devnet/base_test_agent.py')
        self.agents += 1

if __name__ == '__main__':
    unittest.main()