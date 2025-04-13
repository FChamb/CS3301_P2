# Python Publish-Subscribe System - 220010065 #

### Overview ###
This Python code implements a simple publish-subscribe (pub-sub) 
messaging system. The pub-sub pattern is a way to decouple message 
producers (publishers) from message consumers (subscribers). 
Publishers send messages to topics, and subscribers receive 
messages from the topics they are subscribed to. This
implementation fully matches the specification and implements
all the requirements.

### Requirements ###
The system is designed to meet the following requirements:
* **R1**: Subscribing and publishing events
* **R2**: Lookup, discovery, and access of event channels
* **R3**: Dynamic message queue management
* **R4**: Temporary interruptions of connections
* **R5**: Crashing queues
* **R6**: Crashing subscribers
* **R7**: Long delays in network traffic
* **R8**: Dropped messages
* **R9**: Out of order messages
* **R10**: Duplicated messages

### Design and Implementation ###
The system consists of the following components:

* **Message**: Represents a message with a unique ID, topic, 
payload, and timestamp.
* **MessageQueue**: Manages a queue of messages for a specific 
topic. It handles message enqueueing, dequeueing, and 
subscriber management.
* **PubSubSystem**: Manages message queues and provides 
methods for creating queues, publishing messages, and 
subscribing/unsubscribing subscribers.
* **Subscriber**: Represents a message consumer that receives 
messages from subscribed topics.

The system uses threads for message delivery, allowing 
publishers and subscribers to operate concurrently.
Locks are used to ensure thread safety when accessing 
shared resources, such as message queues and subscriber lists.

### How to Run the Code ###
1. Open the project code and cd into src directory.
```console
cd src/
```

2. **Run from the terminal:** You can run the publisher or
subscriber from the terminal using the following commands:
* **Publish:**
```console
python3 main.py publish <topic_name> --messages <#_of_messages>
```
For example:
```console
python3 main.py publish my_topic --messages 10
```
* **Subscribe:**
```console
python3 main.py subscriber <topic_name> --subscriber_name <subscriber_name>
```
For example:
```console
python3 main.py subscribe my_topic --subscriber_name sub1
```

3. **Run test file:** You can run the publisher and subscriber
test file which tests all the practical requirements at once:
```console
python3 test.py
```

### Example ###
1. Open two terminal windows.
2. In the first terminal, run the subscriber:
```console
python3 main.py subsribe my_topic --subscriber_name sub1
```
3. In the second terminal, run the publisher:
```console
python3 main.py publish my_topic --messages 5
```
4. You will see the messages being published in the publisher
terminal and the subscriber receiving them in the subscriber
terminal.