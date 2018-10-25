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
        for i in range(0, 3):
            self.wait_for_response()
            self.assertNotEqual(b'NULL', self.message)
            self.assertLess(15, len(self.message))
            seeds.append(self.message.decode("utf-8"))

        self.assertEqual(3, len(seeds))

        #'["0.0.0.0:7517/j7qWfWaJRVp25ZsnCu9rJ4PmhigZBtesB4YmQHqqPvtR"]' like
        seeders_str = '["' + '","'.join(seeds) + ']"'
        print(seeders_str)

        seeds = []
        for i in range(0, 3):
            self.start_node_agent_pair(seeders_str)

        self.send('GET_NODE_ID')
        for i in range(0, 6):
            self.wait_for_response()
            self.assertNotEqual(b'NULL', self.message)
            self.assertLess(15, len(self.message))
            seeds.append(self.message)

if __name__ == '__main__':
    unittest.main()