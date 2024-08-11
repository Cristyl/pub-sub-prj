import sys
import time
import random
from publisher_handler  import Publisherhandler
from subscriber_handler import Subscriberhandler

random.seed(42)

# create a new publisher or a new subscriber
def create_node(exchanges, id, pids, type):
    exchange_name = random.choice(exchanges)
    command = f'python {type}.py {exchange_name} {id}'
    if (type == 'publisher'):
        publisher_handler.create_publisher(command, pids)
    elif (type == 'subscriber'):
        subscriber_handler.create_subscriber(command, pids)

# delete a publisher or a subscriber
def delete_node(pids, type):
    candidate = random.choice(pids)
    if (type == 'publisher'):
        publisher_handler.kill_publisher(candidate, pids)
        print(f"[main] Killed the Pub with pid {candidate}", flush=True)
    elif (type == 'subscriber'): 
        subscriber_handler.kill_subscriber(candidate, pids)
        # since it's a simulation of a sub crash, this line should be commented at the final version. 
        # The sub process will say "crashed" anyway
        print(f"[main] Killed the Sub with pid {candidate}", flush=True)
            
if __name__ == "__main__":
    # define the number of publishers and subscribers (it can modify the upper and lower bounds)
    if len(sys.argv) != 3 or sys.argv[1].isdigit() == False or sys.argv[2].isdigit() == False:
        print("[main] Usage: python main.py <num_of_pub> <num_of_sub>", flush=True)
        sys.exit(1)

    number_of_publishers  = int(sys.argv[1])
    number_of_subscribers = int(sys.argv[2])

    # list of the exchanges
    exchange_names = ['logs1', 'logs2', 'logs3', 'logs4']

    # lists of the pids of publishers and subscribers
    pids_publishers  = []
    pids_subscribers = []

    # create the publisher and subscriber handlers
    publisher_handler  = Publisherhandler(number_of_publishers, exchange_names)
    subscriber_handler = Subscriberhandler(number_of_subscribers, exchange_names)
    
    print("\n[main] -----------------------------", flush=True)
    print("[main] Simulation start", flush=True)
    print("[main] -----------------------------", flush=True)

    # create the subscribers
    for subscriber_id in range(number_of_subscribers):
        create_node(exchange_names, subscriber_id, pids_subscribers, 'subscriber')

    # create the publishers
    # [we create first the subscribers to not risk to loose any message]
    for publisher_id in range(number_of_publishers):
        create_node(exchange_names, publisher_id, pids_publishers, 'publisher')

    # stay into the while loop till there is a pub or a sub
    while number_of_publishers or number_of_subscribers:
        # with a certain probability kill the sub and pub candidates (the right operator can be modified)
        if number_of_subscribers and (random.uniform(0, 100) < 0.00001):
            number_of_subscribers -= 1
            delete_node(pids_subscribers, 'subscriber')

        if number_of_publishers and (random.uniform(0, 100) < 0.00001):
            number_of_publishers -= 1
            delete_node(pids_publishers, 'publisher')

        # randomly create a new publisher
        if random.uniform(0, 300) < 0.00001:
            create_node(exchange_names, number_of_publishers, pids_publishers, 'publisher')
            print(f"[main] Pub #{number_of_publishers} has joined", flush=True)
            number_of_publishers += 1

        # randomly create a new subscriber      
        if random.uniform(0, 300) < 0.00001:
            create_node(exchange_names, number_of_subscribers, pids_subscribers, 'subscriber')
            print(f"[main] Sub #{number_of_subscribers} has joined", flush=True)
            number_of_subscribers += 1

    print("[main] -----------------------------", flush=True)
    print("[main] Simulation completed", flush=True)
    print("[main] -----------------------------\n", flush=True)