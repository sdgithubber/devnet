from base_test_ci import BaseTest
import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class Test1(BaseTest):
    def test_sendId(self):
        phase_0 = self.create_phase("1")
        self.start_node_agent_pair(bootstrap='false')
        self.send('GET_NODE_ID')
        self.wait_for_response(1)

        self.assertEqual(1, len(self.messages))
        self.assertNotEqual(b'NULL', self.messages[0])
        self.assertLess(15, len(self.messages[0]))

if __name__ == '__main__':
    unittest.main()