import threading
import time
import logging

from message import Message
from messagequeue import MessageQueue
from pubsubsystem import PubSubSystem
from subscriber import (Subscriber, simulate_subscriber_crash, simulate_queue_crash, simulate_network_delay,
                        simulate_message_drop)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_pubsub():
    pubsub = PubSubSystem()
    topic = "test_topic"
    pubsub.create_queue(topic)

    subscriber1 = Subscriber("subscriber1")
    subscriber2 = Subscriber("subscriber2")

    pubsub.subscribe(topic, subscriber1)
    pubsub.subscribe(topic, subscriber2)

    delivery_thread = threading.Thread(target=pubsub.deliver_messages)
    delivery_thread.daemon = True
    delivery_thread.start()

    # Test R1: Subscribing and publishing events
    pubsub.publish(topic, "Message 1")
    pubsub.publish(topic, "Message 2")

    time.sleep(0.1)  # allow delivery

    assert len(subscriber1.received_messages) == 2
    assert len(subscriber2.received_messages) == 2

    # Test R2: Lookup, discovery, and access of event channels
    assert pubsub.get_queue(topic) is not None
    assert pubsub.get_queue("nonexistent_topic") is None

    # Test R3: Dynamic message queue management
    new_topic = "new_topic"
    pubsub.create_queue(new_topic)
    assert pubsub.get_queue(new_topic) is not None

    # Test R4: Temporary interruptions of connections (simulated delay)
    simulate_network_delay(0.01)  # add a little delay.

    # Test R5: Crashing queues
    simulate_queue_crash(pubsub.get_queue(topic))
    pubsub.publish(topic, "Message 3")  # should be discarded during crash
    time.sleep(2.1)  # allow time for recovery and delivery of message after recovery.
    assert len(subscriber1.received_messages) == 3  # message 3 is now expected.

    # Test R6: Crashing customers
    subscriber3 = Subscriber("subscriber3")
    pubsub.subscribe(topic, subscriber3)
    simulate_subscriber_crash(subscriber3, pubsub, topic)
    pubsub.publish(topic, "Message 4")
    time.sleep(6)  # allow recovery and delivery
    assert len(subscriber3.received_messages) == 1

    # Test R8: Dropped messages.
    simulate_message_drop(pubsub, topic, "dropped message", 0.5)
    pubsub.publish(topic, "message 5")
    time.sleep(0.1)
    assert len(subscriber1.received_messages) >= 4  # message 3 is delivered, and message 5 is delivered.

    logging.info("PubSub system tests passed.")


def test_pubsub_performance():
    pubsub = PubSubSystem()
    topic = "performance_topic"
    pubsub.create_queue(topic)

    subscriber = Subscriber("performance_subscriber")
    pubsub.subscribe(topic, subscriber)

    delivery_thread = threading.Thread(target=pubsub.deliver_messages)
    delivery_thread.daemon = True
    delivery_thread.start()

    num_messages = 1000
    start_time = time.time()

    for i in range(num_messages):
        pubsub.publish(topic, f"Message {i}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    messages_per_second = num_messages / elapsed_time

    logging.info(f"Published {num_messages} messages in {elapsed_time:.2f} seconds.")
    logging.info(f"Messages per second: {messages_per_second:.2f}")

    # wait until all messages are recieved.
    while len(subscriber.received_messages) < num_messages:
        time.sleep(0.01)

    assert len(subscriber.received_messages) == num_messages
    assert messages_per_second >= 1000, f"Expected >= 1000 messages/second, got {messages_per_second:.2f}"
    logging.info("Performance test passed.")


if __name__ == "__main__":
    test_pubsub()
    test_pubsub_performance()
