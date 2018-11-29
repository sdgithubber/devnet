from pubsub import PubSub
from google.cloud import pubsub_v1


class GooglePubSub(PubSub):
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.project = "spacemesh-198810"
    
    def Subscribe(self, channel_name, callback):
        topic_path = self.publisher.topic_path(self.project, channel_name)
        subscription_path = self.subscriber.subscription_path(self.project, "kaplan")
        print subscription_path
        self.subscriber.create_subscription(subscription_path, topic_path)
        self.subscriber.subscribe(subscription_path, callback=callback)
    
    def Publish(self, channel_name, **kwargs):
        self.publisher.publish(channel_name, **kwargs)

    def UnSubscribe(self, channel_name):
        self.subscriber.delete_subscription(channel_name)

    def CreateChannel(self, channel_name):
        topic_path = self.publisher.topic_path(self.project, topic_name)
        self.publisher.create_topic(topic_path)
        return tpoic_path


    def DeleteChannel(self, channel_name):
        self.publisher.delete_topic(channel_name)