import config
from google.cloud import pubsub_v1
import time
import re
import datetime
from subprocess import call
import spur

class BaseDevnetAgent:
    def __init__(self):
        self.endFlag = False
    
        project = config.CONFIG['project']
        topic_name_upstream = config.CONFIG['topic_name_upstream']
        self.publisher_upstream = pubsub_v1.PublisherClient()
        self.topic_path_upstream = self.publisher_upstream.topic_path(project, topic_name_upstream)

        subscription_name_downstream = config.CONFIG['subscription_name_downstream']
        self.subscriber_downstream = pubsub_v1.SubscriberClient()
        self.subscription_path_downstream = self.subscriber_downstream.subscription_path(project, subscription_name_downstream)

    def stop_node(self):
        shell = spur.SshShell(
            hostname=config.CONFIG['host'], 
            username=config.CONFIG['host_user'], 
            password=config.CONFIG['host_password'], 
            missing_host_key=spur.ssh.MissingHostKey.accept
        )
        with shell:
            try:
                result = shell.run(["docker", "stop", "node"])
                print('Node stopped: ' + "".join(map(chr, result.output)))
                result = shell.run(["docker", "rm", "node"])
                print('Node removed: ' + "".join(map(chr, result.output)))
            except:
                print('Node stop/remove failed')

    def callback(self, message):
        self.message = message.data
        message.ack()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " GOT_DOWN_MSG " + "".join(map(chr, self.message))) 
        if b'END' == self.message:
            self.stop_node()
            self.endFlag = True
        elif b'SEND_UP' == self.message:
            self.send('UP')
        elif b'GET_NODE_ID' == self.message:
            self.send(self.get_node_id())
        elif b'SHUTDOWN_NODE' == self.message:
            self.stop_node()

    def act_on_request(self):
        self.subscriber_downstream.subscribe(self.subscription_path_downstream, callback=self.callback)
        while not self.endFlag:
            time.sleep(1)

    def send(self, data):
        data = data.encode('utf-8')
        self.publisher_upstream.publish(self.topic_path_upstream, data=data)

    def get_node_id(self):
        time.sleep(15)
        pattern = re.compile(u'.*NodeID (\w+)')
        node_id = 'NULL'
        for line in open('/opt/logs/node.log', "r", encoding="utf-8"):
            results = pattern.match(line)
            if results != None:
                node_id = results.group(1)
                break;
        return node_id


if __name__ == '__main__':
    t = BaseDevnetAgent()
    t.act_on_request()