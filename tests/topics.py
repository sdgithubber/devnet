import config
from google.cloud import pubsub_v1
import logging
from logging import Logger

class Publisher():
    def enable(self, project, topic_name):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project, topic_name)

    def publish(self, **kwargs):
        self.publisher.publish(self.topic_path, **kwargs)

class Subscriber():
    def subscribe(self, project, subscription_name, callback):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project, subscription_name)
        self.subscriber.subscribe(self.subscription_path, callback=callback)