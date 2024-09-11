import random
from publisher_handler  import Publisherhandler
from subscriber_handler import Subscriberhandler
from broker_handler     import Brokerhandler

class CONST(object):

    PUBS_PORT = ["5559", "5561", "5563"]
    SUBS_PORT = ["5560", "5562", "5564"]
    TOPICS    = ['saturn', 'earth', 'mars', 'red']
    KILL_PROBABILITY    = 0.00001
    CREATION_PROBABILIY = 0.000005
    MAX_DURATION        = 60
    MAX_SUB             = 7
    MAX_PUB             = 7
    NUMBER_OF_BROKERS   = 3

    def __setattr__(self, *_):
        pass

CONST = CONST()

# create the broker, publisher and subscriber handlers
publisher_handler  = Publisherhandler()
subscriber_handler = Subscriberhandler()
broker_handler = Brokerhandler()

# create a new publisher or a new subscriber
def create_node(id, type):
    command = ['python3', type + '.py', str(id)]
    if (type == 'publisher'):
        publisher_handler.create_publisher(command)
    elif (type == 'subscriber'):
        subscriber_handler.create_subscriber(command)

# delete a publisher or a subscriber
def delete_node(pid, type, termination=False):
    candidate = pid
    decision = random.uniform(1, 100) > 50
    if (type == 'publisher'):
        if decision or termination:
            publisher_handler.close_publisher(candidate)
        else:
            publisher_handler.kill_publisher(candidate)
    elif (type == 'subscriber'):
        if decision or termination:
            subscriber_handler.close_subscriber(candidate)
        else:
            subscriber_handler.kill_subscriber(candidate)

# creates a topic
def create_topic(type):
    if type == 'publisher':
        topic = random.choice(CONST.TOPICS)
    elif type == 'subscriber':
        topic = []
        for _ in range(random.randint(1, 3)):
            next_topic = random.choice(CONST.TOPICS)
            if next_topic not in topic:
                topic.append(next_topic)
    return topic

# create a new broker
def create_broker(broker_id):
    command = ['python3', 'broker' + '.py', CONST.PUBS_PORT[broker_id], CONST.SUBS_PORT[broker_id], str(broker_id)]
    broker_handler.create_broker(command)

# delete a broker
def delete_broker(pid, terminated=False):
    if terminated:
        broker_handler.close_broker(pid)
    else:
        broker_handler.kill_broker(pid)