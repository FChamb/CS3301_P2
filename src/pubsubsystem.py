import threading
import logging
import time

from message import Message
from messagequeue import MessageQueue


class PubSubSystem:
    def __init__(self):
        self.queues = {}
        self.queue_lock = threading.Lock()
        self.subscribers = {}

    def create_queue(self, queue_name):
        with self.queue_lock:
            if queue_name not in self.queues:
                self.queues[queue_name] = MessageQueue(queue_name)
                return self.queues[queue_name]
            else:
                return self.queues[queue_name]

    def get_queue(self, queue_name):
        with self.queue_lock:
            return self.queues.get(queue_name)

    def publish(self, topic, payload):
        queue = self.get_queue(topic)
        if queue:
            message = Message(topic, payload)
            queue.enqueue(message)
            return message
        else:
            logging.warning(f"Topic '{topic}' does not exist.")
            return None

    def subscribe(self, topic, subscriber):
        queue = self.get_queue(topic)
        if queue:
            queue.add_subscriber(subscriber)
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            self.subscribers[topic].append(subscriber)
            return True
        else:
            logging.warning(f"Topic '{topic}' does not exist.")
            return False

    def unsubscribe(self, topic, subscriber):
        queue = self.get_queue(topic)
        if queue:
            queue.remove_subscriber(subscriber)
            if topic in self.subscribers and subscriber in self.subscribers[topic]:
                self.subscribers[topic].remove(subscriber)
            return True
        else:
            return False

    def deliver_messages(self):
        while True:
            with self.queue_lock:
                for queue in self.queues.values():
                    message = queue.dequeue()
                    if message:
                        for subscriber in queue.subscribers:
                            try:
                                subscriber.receive(message)
                            except Exception as e:
                                logging.error(f"Error delivering message {message.id} to subscriber {subscriber}: {e}")
            # Adjust speed
            time.sleep(0.001)