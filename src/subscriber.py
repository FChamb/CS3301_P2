import random
import time
import logging


class Subscriber:
    def __init__(self, name):
        self.name = name
        self.received_messages = []

    def receive(self, message):
        self.received_messages.append(message)
        logging.info(f"Subscriber '{self.name}': Received message {message.id}")


# Fault injection and testing functions
def simulate_network_delay(delay):
    time.sleep(delay)


def simulate_queue_crash(queue):
    queue.crash()
    time.sleep(2)
    queue.recover()


def simulate_subscriber_crash(subscriber, pubsub, topic):
    logging.error(f"Subscriber '{subscriber.name}' crashed.")
    pubsub.unsubscribe(topic, subscriber)
    time.sleep(5)
    pubsub.subscribe(topic, subscriber)
    logging.info(f"Subscriber '{subscriber.name}' recovered.")


def simulate_message_drop(pubsub, topic, payload, drop_probability):
    if random.random() < drop_probability:
        logging.warning(f"Message dropped: {payload}")
        return None
    else:
        return pubsub.publish(topic, payload)
