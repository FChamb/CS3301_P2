import threading
import logging


class MessageQueue:
    def __init__(self, name):
        self.name = name
        self.queue = []
        self.lock = threading.Lock()
        self.subscribers = []
        self.crashed = False

    def enqueue(self, message):
        with self.lock:
            if not self.crashed:
                self.queue.append(message)
                logging.info(f"Queue '{self.name}': Enqueued message {message.id}")
                return True
            else:
                logging.warning(f"Queue '{self.name}' is crashed, message {message.id} discarded.")
                return False

    def dequeue(self):
        with self.lock:
            if self.queue and not self.crashed:
                return self.queue.pop(0)
            else:
                return None

    def add_subscriber(self, subscriber):
        with self.lock:
            self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        with self.lock:
            if subscriber in self.subscribers:
                self.subscribers.remove(subscriber)

    def crash(self):
        with self.lock:
            self.crashed = True
            logging.error(f"Queue '{self.name}' crashed.")

    def recover(self):
        with self.lock:
            self.crashed = False
            logging.info(f"Queue '{self.name}' recovered.")
