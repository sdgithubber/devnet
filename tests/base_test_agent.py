import config
from google.cloud import pubsub_v1

class BaseDevnetAGent:
    def __init__(self):
        project = config.CONFIG['project']
        topic_name = config.CONFIG['topic_name']
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project, topic_name)

    def send(self, data):
        data = data.encode('utf-8')
        self.publisher.publish(self.topic_path, data=data)

if __name__ == '__main__':
    t = BaseDevnetAGent()
    t.send('UP')