import uuid
import time


class Message:
    def __init__(self, topic, payload):
        self.id = uuid.uuid4()
        self.topic = topic
        self.payload = payload
        self.timestamp = time.time()
        # For dropped message retries
        self.attempts = 0

    def __str__(self):
        return f"Message(id={self.id}, topic='{self.topic}', payload='{self.payload}', timestamp={self.timestamp})"
