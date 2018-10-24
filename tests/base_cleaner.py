import config
from google.cloud import pubsub_v1
import time

class BaseDevnetCleaner:
    def __init__(self):
        self.endFlag = False
    
        self.project = config.CONFIG['project']

        subscription_name_upstream = config.CONFIG['subscription_name_upstream']
        self.subscriber_upstream = pubsub_v1.SubscriberClient()
        self.subscription_path_upstream = self.subscriber_upstream.subscription_path(self.project, subscription_name_upstream)

        self.subscriber_downstream = pubsub_v1.SubscriberClient()

    def get_downstream_subscription_path(self, i):
        return self.subscriber_downstream.subscription_path(self.project, config.CONFIG['subscription_name_downstream'] + '_' + str(i))

    def callback(self, message):
        self.endFlag = False
        message.ack()

    def cleanup(self, subscriber, subscription_path):
        subscriber.subscribe(subscription_path, callback=self.callback)
        while not self.endFlag:
            self.endFlag = True
            time.sleep(1)

if __name__ == '__main__':
    t = BaseDevnetCleaner()

    for i in range(0, 10):
        t.cleanup(t.subscriber_downstream, t.get_downstream_subscription_path(i))
    t.cleanup(t.subscriber_upstream, t.subscription_path_upstream)