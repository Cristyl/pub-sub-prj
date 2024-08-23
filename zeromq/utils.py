import random

from publisher_handler  import Publisherhandler
from subscriber_handler  import Subscriberhandler
from broker_handler import Brokerhandler


class CONST(object):

    PUBS_PORT = "5559"
    SUBS_PORT = "5560"
    TOPIC = ['saturn', 'earth', 'mars', 'red', 'blue', 'grey', 'indie', 'rock', 'soul']
    KILL_PROBABILITY    = 0.00001
    CREATION_PROBABILIY = 0.000005
    MAX_DURATION        = 60

    def __setattr__(self, *_):
        pass

CONST = CONST()

# create the broker, publisher and subscriber handlers
publisher_handler  = Publisherhandler()
subscriber_handler = Subscriberhandler()
broker_handler = Brokerhandler()

# create a new publisher or a new subscriber
def create_node(port, id, type):
    topic = create_topic(type)
    command = ['python3', type + '.py', port, str(id)]
    if (type == 'publisher'):
        publisher_handler.create_publisher(command)
    elif (type == 'subscriber'):
        subscriber_handler.create_subscriber(command)

# delete a publisher or a subscriber
def delete_node(pid, type):
    candidate = pid
    if (type == 'publisher'):
        publisher_handler.kill_publisher(candidate)
    elif (type == 'subscriber'):
        subscriber_handler.kill_subscriber(candidate)

# creates a topic
def create_topic(type):
    if type == 'publisher':
        topic = random.choice(CONST.TOPIC)
    elif type == 'subscriber':
        topic = []
        for _ in range(random.randint(1, 3)):
            next_topic = random.choice(CONST.TOPIC)
            if next_topic not in topic:
                topic.append(next_topic)
    return topic

def create_broker():
    command = ['python3', 'broker' + '.py', CONST.PUBS_PORT, CONST.SUBS_PORT]
    broker_handler.create_broker(command)

def delete_broker():
    broker_handler.kill_broker()