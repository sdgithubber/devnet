from base_test_ci import BaseTest
import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class Test1(BaseTest):
    def test_sendId(self):
        messages = self.run_phase(nodes = 1, bootstrap = 'false', message = 'GET_NODE_ID')
        self.assertLess(15, len(messages[0]))

if __name__ == '__main__':
    unittest.main()