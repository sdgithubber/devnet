import os
import time
from google.cloud import pubsub_v1
import unittest

class Test0(unittest.TestCase):
    def setUp(self):
        self.testLen = 10
        self.message = ''
        project = 'spacemesh-198810'
        subscription_name = 'devnet_tests_ci'
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project, subscription_name)

    def callback(message):
        self.message = '{}'.format(message)
        message.ack()

    def test_verifyHi(self):
        subscriber.subscribe(subscription_path, callback=self.callback)
        print('Listening for messages on {}'.format(subscription_path))
        time.sleep(self.testLen)
        self.assertEquals('UP', self.message)

if __name__ == '__main__':
    unittest.main()