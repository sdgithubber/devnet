import config
import os
import time
from google.cloud import pubsub_v1
import unittest
import spur

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.endFlag = False
        self.testLen = 20
        self.message = b'NULL'
        project = config.CONFIG['project']
        subscription_name_upstream = config.CONFIG['subscription_name_upstream']
        self.subscriber_upstream = pubsub_v1.SubscriberClient()
        self.subscription_path_upstream = self.subscriber_upstream.subscription_path(project, subscription_name_upstream)
        self.subscriber_upstream.subscribe(self.subscription_path_upstream, callback=self.callback)

        topic_name_downstream = config.CONFIG['topic_name_downstream']
        self.publisher_downstream = pubsub_v1.PublisherClient()
        self.topic_path_downstream = self.publisher_downstream.topic_path(project, topic_name_downstream)

    def tearDown(self):
        self.send('END')

    def callback(self, message):
        self.message = message.data
        message.ack()
        self.endFlag = True

    def send(self, data):
        data = data.encode('utf-8')
        self.publisher_downstream.publish(self.topic_path_downstream, data=data)

    def wait_for_response(self):
        for i in range(0, self.testLen):
            if self.endFlag:
                print(self.message)
                break
            time.sleep(1)

    def send_and_wait(self, data):
        self.send(data)
        self.wait_for_response()

    def start_node_agent_pair(self):
        shell = spur.SshShell(
            hostname=config.CONFIG['host'], 
            username=config.CONFIG['host_user'], 
            password=config.CONFIG['host_password'], 
            missing_host_key=spur.ssh.MissingHostKey.accept
        )
        with shell:
            try:
                cmd = 'docker run --rm --network=devnet --name node -p 7513:7513 spacemesh/node:latest /go/src/github.com/spacemeshos/go-spacemesh/go-spacemesh >> /root/spacemesh/devnet/logs/node.log 2>&1 &'
                print(cmd)
                result = shell.run(cmd.split(' '))
                print('Node started: ' + "".join(map(chr, result.output)))
                cmd = 'docker run --rm --network=devnet --name agent -p 8080:8080 -v /root/spacemesh/devnet/tests:/opt/devnet -v /root/spacemesh/devnet/logs:/opt/logs spacemesh/devnet_agent:latest python3 /opt/devnet/base_test_agent.py >> /root/spacemesh/devnet/logs/test.log 2>&1 &'
                print(cmd)
                print('Agent started: ' + "".join(map(chr, result.output)))
            except Exception as e:
                print('Node/Agent started failed')
                print(e.__doc__ )
                print(e.message)

if __name__ == '__main__':
    unittest.main()