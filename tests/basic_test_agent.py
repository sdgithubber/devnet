# [START app]
#import base64
#import json
#import logging
#import os
#import json

from google.cloud import pubsub_v1

project = 'spacemesh-198810'
topic_name = 'devnet_tests'
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project, topic_name)
data = ' '
data = data.encode('utf-8')
publisher.publish(topic_path, data=data)