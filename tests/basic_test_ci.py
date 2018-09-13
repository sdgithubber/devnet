import os
import time

from google.cloud import pubsub_v1
project = 'spacemesh-198810'
subscription_name = 'devnet_tests_ci'
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project, subscription_name)

def callback(message):
    print('Received message: {}'.format(message))
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)

# The subscriber is non-blocking, so we must keep the main thread from
# exiting to allow it to process messages in the background.
print('Listening for messages on {}'.format(subscription_path))
while True:
    print("in the loop")
    time.sleep(60)