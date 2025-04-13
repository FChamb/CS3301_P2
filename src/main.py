import time
import logging
import argparse
import threading

from subscriber import Subscriber
from pubsubsystem import PubSubSystem

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Fault injection and testing functions
# ... (Fault injection functions remain the same)
def run_publisher(pubsub, topic, message_count):
    for i in range(message_count):
        pubsub.publish(topic, f"Message {i}")
        # Add a small delay for better observation
        time.sleep(0.01)


def run_subscriber(pubsub, topic, subscriber_name):
    subscriber = Subscriber(subscriber_name)
    pubsub.subscribe(topic, subscriber)
    logging.info(f"Subscriber '{subscriber_name}' subscribed to topic '{topic}'.")

    try:
        while True:
            # Keep the subscriber alive
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info(f"Subscriber '{subscriber_name}' unsubscribed.")
        pubsub.unsubscribe(topic,subscriber)


def main():
    parser = argparse.ArgumentParser(description="Pub-Sub System CLI")
    parser.add_argument("mode", choices=["publish", "subscribe"], help="Mode: publish or subscribe")
    parser.add_argument("topic", help="Topic name")
    parser.add_argument("--messages", type=int, default=1, help="Number of messages to publish (for publish mode)")
    parser.add_argument("--subscriber_name", type=str, default="cli_subscriber", help="Subscriber name (for subscribe mode)")

    args = parser.parse_args()

    pubsub = PubSubSystem()
    # Create the queue before publisher or subscriber run
    pubsub.create_queue(args.topic)

    delivery_thread = threading.Thread(target=pubsub.deliver_messages)
    delivery_thread.daemon = True
    delivery_thread.start()

    if args.mode == "publish":
        run_publisher(pubsub, args.topic, args.messages)
        logging.info(f"{args.messages} messages published to topic '{args.topic}'.")
    elif args.mode == "subscribe":
        run_subscriber(pubsub, args.topic, args.subscriber_name)


if __name__ == "__main__":
    main()
