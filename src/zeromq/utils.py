import random

from publisher_handler  import Publisherhandler
from broker_handler import Brokerhandler

random.seed(42)

class CONST(object):

    TOPIC1         = ['saturn', 'earth', 'mars', '*', '#']
    TOPIC2         = ['red', 'blue', 'grey', '*', '#']
    TOPIC3         = ['indie', 'rock', 'soul', '*']
    KILL_PROBABILITY    = 0.00001
    CREATION_PROBABILIY = 0.000005
    MAX_DURATION        = 60

    def __setattr__(self, *_):
        pass

CONST = CONST()

# create the publisher and subscriber handlers
publisher_handler  = Publisherhandler()
broker_handler = Brokerhandler()

# create a new publisher or a new subscriber
def create_node(id, port, type):
    command = ['python3', type + '.py', port, str(id)]
    if (type == 'publisher'):
        publisher_handler.create_publisher(command)

# delete a publisher or a subscriber
def delete_node(pid, type):
    candidate = pid
    if (type == 'publisher'):
        publisher_handler.kill_publisher(candidate)

def create_broker():
    command = ['python3', 'broker' + '.py', broker_handler.pub_port, broker_handler.sub_port]
    broker_handler.create_broker(command)

def delete_broker():
    broker_handler.kill_broker()