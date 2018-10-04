from base_test_ci import BaseTest
import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class Test0(BaseTest):
    def test_verifyUp(self):
        self.subscriber.subscribe(self.subscription_path, callback=self.callback)
        for i in range(0, self.testLen):
            if self.endFlag:
                break
            time.sleep(1)

        self.assertEqual(b'UP', self.message)

if __name__ == '__main__':
    unittest.main()