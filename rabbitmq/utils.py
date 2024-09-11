import random
from publisher_handler  import Publisherhandler
from subscriber_handler import Subscriberhandler

class CONST(object):

    EXCHANGE_NAME = 'logs'
    TOPIC1         = ['saturn', 'earth', 'mars', '*', '#']
    TOPIC2         = ['red', 'blue', 'grey', '*', '#']
    TOPIC3         = ['indie', 'rock', 'soul', '*', '#']
    KILL_PROBABILITY    = 0.00001
    CREATION_PROBABILIY = 0.000005
    MAX_DURATION        = 60
    MAX_SUB             = 7
    MAX_PUB             = 7

    def __setattr__(self, *_):
        pass

CONST = CONST()

# create the publisher and subscriber handlers
publisher_handler  = Publisherhandler()
subscriber_handler = Subscriberhandler()

# create a new publisher or a new subscriber
def create_node(id, type):
    topic = create_topic(type)
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
        if decision and termination:
            publisher_handler.close_publisher(candidate)
        else:
            publisher_handler.kill_publisher(candidate)
    elif (type == 'subscriber'):
        if decision:
            subscriber_handler.close_subscriber(candidate)
        else:
            subscriber_handler.kill_subscriber(candidate)

# creates a topic
# [a topic exchange with only the '#' binding, becomes a fanout exchange]
# [a topic exchange without '#' and '*' bindings, becomes a direct exchange]
def create_topic(type):
    topic = compose_topic()
    if type == 'subscriber' and topic != '#':
        # creating more than one binding for that sub
        for _ in range(random.randint(0, 2)):
            next_topic = compose_topic()
            if next_topic == '#':
                return '#'
            if topic != next_topic:
                topic += ' ' + next_topic
    return topic

def compose_topic():
    label = random.choice(CONST.TOPIC1)
    topic = label
    if label == '#':
        return topic

    label = random.choice(CONST.TOPIC2)
    topic += ('.' + label)
    if label == '#':
        if topic[0] == '*':
            return '#'
        return topic

    label = random.choice(CONST.TOPIC3)
    if label == '#' and topic[0] == '*' and topic [1] == '*' or label == '*':
        return '#'
    topic += ('.' + label)

    return topic