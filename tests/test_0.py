from base_test_ci import BaseTest
import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class Test0(BaseTest):
    def test_verifyUp(self):
        messages = self.run_phase(nodes = 1, bootstrap = 'false')
        messages = self.send_and_wait('GET_DHT_SIZE', testers_nodes)
        self.assertEqual('UP', messages[0])

if __name__ == '__main__':
    unittest.main()