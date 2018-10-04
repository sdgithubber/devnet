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

    def callback(self, message):
        self.message = message.data
        message.ack()
        self.endFlag = True

if __name__ == '__main__':
    unittest.main()