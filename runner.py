from google_pubsub import GooglePubSub
import time
import pubsub


def PubSubFactory(provider):
        if provider == "google":
            return GooglePubSub()


def printlogs(message):
    print message

if __name__ == '__main__':
    pubsub = PubSubFactory("google")
    pubsub.Subscribe("devnet_tests_downstream", printlogs)
    while True:
        time.sleep(1)
