from base_test_ci import BaseTest
import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class Test1(BaseTest):
    def test_sendId(self):
        self.start_node_agent_pair()
        self.send_and_wait('GET_NODE_ID')

        self.assertNotEqual(b'NULL', self.message)
        self.assertLess(5, len(self.message))

if __name__ == '__main__':
    unittest.main()