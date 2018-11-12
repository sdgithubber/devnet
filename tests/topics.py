import config
import random
import calendar, time
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
    def subscribe(self, project, topic_name, callback):
        self.publisher = pubsub_v1.PublisherClient()
        topic_path = self.publisher.topic_path(project, topic_name)

        self.subscriber = pubsub_v1.SubscriberClient()
        subscription_name = 'devnet_sub_' + str(random.randint(0, 9999999999)) + '_' + str(calendar.timegm(time.gmtime()))
        self.subscription_path = self.subscriber.subscription_path(project, subscription_name)
        subscription = self.subscriber.create_subscription(self.subscription_path, topic_path)
        self.subscriber.subscribe(self.subscription_path, callback=callback)

    def delete(self):
        self.subscriber.delete_subscription(self.subscription_path)