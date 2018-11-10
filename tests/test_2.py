from base_test_ci import BaseTest
import config
import os
import time
import calendar
from google.cloud import pubsub_v1
import unittest
import logging

class Test2(BaseTest):
    def test_sendId(self):
        seeders_nodes = 3
        testers_nodes = 3

        messages = self.run_phase(self, nodes = 3, bootstrap = 'true', message = 'GET_NODE_ID')
        for i in range(0, seeders_nodes):
            self.assertLess(15, len(messages[i]))

        #'["0.0.0.0:7517/j7qWfWaJRVp25ZsnCu9rJ4PmhigZBtesB4YmQHqqPvtR"]' like
        seeders_str = '\'["' + '","'.join(self.messages) + '"]\''
        logging.info(seeders_str)
        messages = self.run_phase(self, nodes = 3, bootstrap = 'true', seeders = seeders_str, message = 'GET_DHT_SIZE')

        for i in range(0, testers_nodes):
            self.assertEqual(seeders_nodes + testers_nodes, int(messages[i]))

if __name__ == '__main__':
    unittest.main()