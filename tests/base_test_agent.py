import config
from google.cloud import pubsub_v1

project = config.CONFIG['project']
subscription_name = config.CONFIG['subscription_name']
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project, topic_name)
data = 'UP'
data = data.encode('utf-8')
publisher.publish(topic_path, data=data)