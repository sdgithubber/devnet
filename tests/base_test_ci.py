import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.endFlag = False
        self.testLen = 20
        self.message = b'NULL'
        project = config.CONFIG['project']
        subscription_name_upstream = config.CONFIG['subscription_name_upstream']
        self.subscriber_upstream = pubsub_v1.SubscriberClient()
        self.subscription_path_upstream = self.subscriber_upstream.subscription_path(project, subscription_name_upstream)

        topic_name_downstream = config.CONFIG['topic_name_downstream']
        self.publisher_downstream = pubsub_v1.PublisherClient()
        self.topic_path_downstream = self.publisher_downstream.topic_path(project, topic_name_downstream)

    def callback(self, message):
        self.message = message.data
        message.ack()
        self.endFlag = True

    def send(self, data):
        data = data.encode('utf-8')
        self.publisher_downstream.publish(self.topic_path_downstream, data=data)

if __name__ == '__main__':
    unittest.main()