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
        phase_0 = self.create_phase("2.0")
        for i in range(0, 3):
            self.start_node_agent_pair(bootstrap='true')
        self.send('GET_NODE_ID')
        logging.info('Xa')
        self.wait_for_response(3)
        logging.info('Xb')

        self.assertEqual(3, len(self.messages))
        for i in range(0, 3):
            self.assertNotEqual(b'NULL', self.messages[i])
            self.assertLess(15, len(self.messages[i]))
        logging.info('Xc')

        #'["0.0.0.0:7517/j7qWfWaJRVp25ZsnCu9rJ4PmhigZBtesB4YmQHqqPvtR"]' like
        phase_1 = self.create_phase("2.1")
        seeders_str = '\'["' + '","'.join(self.messages) + '"]\''
        logging.info(seeders_str)
        logging.info(self.messages)
        self.messages = []
        logging.info(self.messages)

        for i in range(0, 3):
            self.start_node_agent_pair(seeders=seeders_str, bootstrap='true')
        self.send('GET_NODE_ID')
        self.wait_for_response(3)

        logging.info(self.messages)
        self.assertEqual(3, len(self.messages))
        for i in range(0, 3):
            self.assertNotEqual(b'NULL', self.messages[i])
            self.assertLess(15, len(self.messages[i]))

        self.messages = []
        logging.info('Xx')
        self.send('GET_DHT')
        self.wait_for_response(3)
        logging.info('Xy')
        self.assertEqual(3, len(self.messages))
        for i in range(0, 3):
            self.assertEqual(6, self.messages[i])
        logging.info('Xz')
        self.phase = phase_0
        self.send("END")
        self.phase = phase_1
        self.send("END")
if __name__ == '__main__':
    unittest.main()