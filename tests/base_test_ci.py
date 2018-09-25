import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class Test0(unittest.TestCase):
    def setUp(self):
        self.endFlag = False
        self.testLen = 10
        self.message = ''
        project = config.CONFIG['project']
        subscription_name = config.CONFIG['subscription_name']
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project, subscription_name)

    def callback(self, message):
        self.message = message.data
        message.ack()
        self.endFlag = True

    def test_verifyUp(self):
        self.subscriber.subscribe(self.subscription_path, callback=self.callback)
        for i in range(0, self.testLen):
            if self.endFlag:
                self.assertEqual(b'UP', self.message)
                return
            time.sleep(1)

if __name__ == '__main__':
    unittest.main()