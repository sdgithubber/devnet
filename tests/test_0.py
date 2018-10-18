from base_test_ci import BaseTest
import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class Test0(BaseTest):
    def test_verifyUp(self):
        self.start_node_agent_pair()
        self.send_and_wait('SEND_UP')
        
        self.assertEqual(b'UP', self.message)

if __name__ == '__main__':
    unittest.main()