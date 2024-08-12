import random

random.seed(42)

#possible arguments for the topic
topic1 = ['q', 'w', 'e', '*', '#']
topic2 = ['r', 't', 'y', '*', '#']
topic3 = ['u', 'i', 'o', '*']

def exchange_names():
    return ['logs1', 'logs2', 'logs3', 'logs4']

def kill_probability():
    return 0.00001

def creation_probability():
    return 0.000005

def max_duration():
    return 60

#function that creates topics ['#' as topic is equal to having a fanout]
def create_topic(type):
    topic = create_single_topic()
    if type == 'subscriber':
        for _ in range(random.randint(0, 2)):
            topic += ' ' + create_single_topic()
        return topic
    elif type == 'publisher':
        return topic

def create_single_topic():
    topic = ''
    chosen_topic1 = random.choice(topic1)
    topic += chosen_topic1
    if chosen_topic1 == '#':
        return topic
    
    chosen_topic2 = random.choice(topic2)
    topic += '.' + chosen_topic2
    if chosen_topic2 == '#':
        return topic
    
    topic += '.' + random.choice(topic3)
    return topic