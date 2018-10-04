import config
from google.cloud import pubsub_v1
import time
import re

class BaseDevnetAgent:
    def __init__(self):
        project = config.CONFIG['project']
        topic_name_upstream = config.CONFIG['topic_name_upstream']
        self.publisher_upstream = pubsub_v1.PublisherClient()
        self.topic_path_upstream = self.publisher_upstream.topic_path(project, topic_name_upstream)

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
#    t.send('UP')
    t.send(t.get_node_id())