from base_test_ci import BaseTest
import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class Test0(BaseTest):
    def test_verifyUp(self):
        phase_0 = self.create_phase("0")
        self.start_node_agent_pair(bootstrap='false')
        self.send('SEND_UP')
        self.wait_for_response(1)

        self.assertEqual(1, len(self.messages))
        self.assertEqual(b'UP', self.messages[0])

if __name__ == '__main__':
    unittest.main()