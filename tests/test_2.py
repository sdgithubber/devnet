from base_test_ci import BaseTest
import config
import os
import time
from google.cloud import pubsub_v1
import unittest

class Test2(BaseTest):
    def test_sendId(self):
        seeds = []
        for i in range(0, 3):
            self.start_node_agent_pair()
        self.send('GET_NODE_ID')
        self.wait_for_response(3)
        
        self.assertEqual(3, len(self.messages))
        for i in range(0, 3):
            self.assertNotEqual(b'NULL', self.messages[i])
            self.assertLess(15, len(self.messages[i]))
            seeds.append(self.messages[i])

        #'["0.0.0.0:7517/j7qWfWaJRVp25ZsnCu9rJ4PmhigZBtesB4YmQHqqPvtR"]' like
        seeders_str = '["' + '","'.join(self.messages) + ']"'
        print(seeders_str)
        self.messages = []

        for i in range(0, 3):
            self.start_node_agent_pair(seeders_str)
        self.wait_for_response(3)

        self.assertEqual(3, len(self.messages))
        for i in range(0, 6):
            self.assertNotEqual(b'NULL', self.messages[i])
            self.assertLess(15, len(self.messages[i]))

if __name__ == '__main__':
    unittest.main()