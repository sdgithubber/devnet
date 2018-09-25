import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.endFlag = False
        self.testLen = 60
        self.message = ''
        project = config.CONFIG['project']
        subscription_name = config.CONFIG['subscription_name']
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project, subscription_name)

    def callback(self, message):
        self.message = message.data
        message.ack()
        self.endFlag = True

if __name__ == '__main__':
    unittest.main()