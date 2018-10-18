import config
from google.cloud import pubsub_v1
import time

class BaseDevnetCleaner:
    def __init__(self):
        self.endFlag = False
    
        project = config.CONFIG['project']

        subscription_name_upstream = config.CONFIG['subscription_name_upstream']
        self.subscriber_upstream = pubsub_v1.SubscriberClient()
        self.subscription_path_upstream = self.subscriber_upstream.subscription_path(project, subscription_name_upstream)
        
        self.subscriber_downstream = pubsub_v1.SubscriberClient()

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

    subscription_name_downstream = config.CONFIG['subscription_name_downstream']
    for i in range(0, 10):
        t.subscription_path_downstream = t.subscriber_downstream.subscription_path(project, subscription_name_downstream + '_' + str(i))
        t.cleanup(t.subscriber_downstream, t.subscription_path_downstream)
    t.cleanup(t.subscriber_upstream, t.subscription_path_upstream)