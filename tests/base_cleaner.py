import config
from google.cloud import pubsub_v1

class BaseDevnetCleaner:
    def __init__(self):
        self.endFlag = False
    
        project = config.CONFIG['project']

        subscription_name_upstream = config.CONFIG['subscription_name_upstream']
        self.subscriber_upstream = pubsub_v1.SubscriberClient()
        self.subscription_path_downstream = self.subscriber_upstream.subscription_path(project, subscription_name_upstream)

        subscription_name_downstream = config.CONFIG['subscription_name_downstream']
        self.subscriber_downstream = pubsub_v1.SubscriberClient()
        self.subscription_path_downstream = self.subscriber_downstream.subscription_path(project, subscription_name_downstream)

    def callback(self, message):
        self.endFlag = False
        message.ack()

    def cleanup(self, subscriber, subscription_path):
        self.subscriber.subscribe(self.subscription_path, callback=self.callback)
        while not self.endFlag:
            self.endFlag = True
            time.sleep(2)

if __name__ == '__main__':
    t = BaseDevnetCleaner()
    t.cleanup(subscriber_downstream, subscription_path_downstream)
    t.cleanup(subscriber_upstream, subscription_path_upstream)