import config
from google.cloud import pubsub_v1
import time
import re

class BaseDevnetAgent:
    def __init__(self):
        project = config.CONFIG['project']
        topic_name = config.CONFIG['topic_name']
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project, topic_name)

    def send(self, data):
        data = data.encode('utf-8')
        self.publisher.publish(self.topic_path, data=data)

    def get_node_id(self):
        time.sleep(15)
        pattern = re.compile("[.]*NodeID (\w+)")
        node_id = 'NULL'
        for line in open('/opt/logs/node.log', "r", encoding="utf-8"):
            results = pattern.match(line)
            print("results:" + line.encode('utf-8').decode())
            if results != None:
                print("results2:" + results.group(1))
                node_id = results.group(1)
                break;
        return node_id


if __name__ == '__main__':
    t = BaseDevnetAgent()
#    t.send('UP')
    t.send(t.get_node_id())