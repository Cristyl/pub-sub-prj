import sys
import time
import random
from publisher_handler  import Publisherhandler
from subscriber_handler import Subscriberhandler
import utils

random.seed(42)

# create a new publisher or a new subscriber
def create_node(exchanges, id, type):
    topic = utils.create_topic(type)
    exchange_name = random.choice(exchanges)
    command = f'python {type}.py {exchange_name} {id} {topic}'
    if (type == 'publisher'):
        publisher_handler.create_publisher(command)
    elif (type == 'subscriber'):
        subscriber_handler.create_subscriber(command)

# delete a publisher or a subscriber
def delete_node(pids, type):
    candidate = random.choice(pids)
    if (type == 'publisher'):
        publisher_handler.kill_publisher(candidate)
        print(f"[main] Killed the Pub with pid {candidate}", flush=True)
    elif (type == 'subscriber'): 
        subscriber_handler.kill_subscriber(candidate)
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
    exchange_names = utils.exchange_names()

    # create the publisher and subscriber handlers
    publisher_handler  = Publisherhandler()
    subscriber_handler = Subscriberhandler()
    
    print("\n[main] -----------------------------", flush=True)
    print("[main] Simulation start", flush=True)
    print("[main] -----------------------------", flush=True)

    # create the subscribers
    for subscriber_id in range(number_of_subscribers):
        create_node(exchange_names, subscriber_id, 'subscriber')

    # create the publishers
    # [we create first the subscribers to not risk to loose any message]
    for publisher_id in range(number_of_publishers):
        create_node(exchange_names, publisher_id, 'publisher')

    start_time = time.time()
    # stay into the while loop till there is a pub or a sub
    while number_of_publishers or number_of_subscribers:
        # with a certain probability kill the sub and pub candidates (the right operator can be modified)
        if number_of_subscribers and (random.uniform(0, 100) < utils.kill_probability()):
            number_of_subscribers -= 1
            delete_node(subscriber_handler.pids, 'subscriber')

        if number_of_publishers and (random.uniform(0, 100) < utils.kill_probability()):
            number_of_publishers -= 1
            delete_node(publisher_handler.pids, 'publisher')

        # randomly create a new publisher
        if random.uniform(0, 100) < utils.creation_probability():
            create_node(exchange_names, number_of_publishers, 'publisher')
            print(f"[main] Pub #{number_of_publishers} has joined", flush=True)
            number_of_publishers += 1

        # randomly create a new subscriber      
        if random.uniform(0, 100) < utils.creation_probability():
            create_node(exchange_names, number_of_subscribers, 'subscriber')
            print(f"[main] Sub #{number_of_subscribers} has joined", flush=True)
            number_of_subscribers += 1

        #end the simulation after a certain time [works for few pub/sub but not for longer ones]
        if time.time() - start_time >= utils.max_duration():
            print("[main] Execution time (60s) terminated", flush=True)
            for subscriber in subscriber_handler.pids:
                subscriber_handler.kill_subscriber(subscriber)
                print(f"[main] Killed the Sub with pid {subscriber}", flush=True)
            for publisher in publisher_handler.pids:
                publisher_handler.kill_publisher(publisher)
                print(f"[main] Killed the Pub with pid {publisher}", flush=True)
            break
    print("[main] -----------------------------", flush=True)
    print("[main] Simulation completed", flush=True)
    print("[main] -----------------------------\n", flush=True)