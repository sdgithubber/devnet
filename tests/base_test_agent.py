import config
from google.cloud import pubsub_v1
import time
import re

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

    def callback(self, message):
        self.message = message.data
        message.ack()
        print(self.message) 
        if b'END' == self.message:
            self.endFlag = True
        if b'SEND_UP' == self.message:
            self.send('UP')
        if b'GET_NODE_ID' == self.message:
            self.send(self.get_node_id())

    def act_on_request():
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