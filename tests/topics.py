import config
import random
import calendar, time
from google.cloud import pubsub_v1
import logging
from logging import Logger

class Publisher():
    def __init__(self, project, topic_path = ''):
        self.project = project
        self.topic_path = topic_path
        self.publisher = pubsub_v1.PublisherClient()

    def create(self):
        self.subscribers = []
        topic_name = 'devnet_topic_' + str(random.randint(0, 9999999999)) + '_' + str(calendar.timegm(time.gmtime()))
        self.topic_path = self.publisher.topic_path(self.project, topic_name)
        self.publisher.create_topic(self.topic_path)
        return self.topic_path

    def publish(self, **kwargs):
        self.publisher.publish(self.topic_path, **kwargs)

    def add_subscription(self):
        subscriber = Subscriber(self.project)
        subscriber.create_for_publisher(self.topic_path)
        self.subscribers.append(subscriber)
        return subscriber

    def delete(self):
        for s in self.subscribers:
            s.delete()
        self.publisher.delete_topic(self.topic_path)

class Subscriber():
    def __init__(self, project, subscription_path = ''):
        self.project = project
        self.subscription_path = subscription_path
        self.subscriber = pubsub_v1.SubscriberClient()

    def create(self, topic_name):
        self.publisher = pubsub_v1.PublisherClient()
        topic_path = self.publisher.topic_path(self.project, topic_name)
        return self.create_for_publisher(self, topic_path)

    def create_for_publisher(self, topic_path):
        self.subscription_name = 'devnet_sub_' + str(random.randint(0, 9999999999)) + '_' + str(calendar.timegm(time.gmtime()))
        self.subscription_path = self.subscriber.subscription_path(self.project, self.subscription_name)
        self.subscriber.create_subscription(self.subscription_path, topic_path)
        return self.subscription_name

    def subscribe(self, callback):
        self.subscriber.subscribe(self.subscription_path, callback=callback)

    def delete(self):
        self.subscriber.delete_subscription(self.subscription_path)