from base_test_ci import BaseTest
import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class Test1(BaseTest):
    def test_sendId(self):
        self.subscriber.subscribe(self.subscription_path, callback=self.callback)
        for i in range(0, self.testLen):
            if self.endFlag:
                print(self.message)
                break
            time.sleep(1)

        self.assertNotEqual('NULL', self.message)
        self.assertGreater(5, len(self.message))

if __name__ == '__main__':
    unittest.main()