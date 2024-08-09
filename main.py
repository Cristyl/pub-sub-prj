import sys
import time
import random
from publisher_handler  import Publisherhandler
from subscriber_handler import Subscriberhandler

random.seed(42)

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
    
    print("[main] -----------------------------", flush=True)
    print("[main] Simulation start", flush=True)
    print("[main] -----------------------------", flush=True)

    # create the subscribers
    for subscriber_id in range(number_of_subscribers):
        exchange_name = random.choice(exchange_names)
        command = f'python subscriber.py {exchange_name} {subscriber_id}'
        subscriber_handler.create_subscriber(command, pids_subscribers)

    # create the publishers
    # [we create first the subscribers to not risk to loose any message]
    for publisher_id in range(number_of_publishers):
        exchange_name = random.choice(exchange_names)
        command = f'python publisher.py {exchange_name} {publisher_id}'
        publisher_handler.create_publisher(command, pids_publishers)

    # stay into the while loop till there are a pub or a sub
    while number_of_publishers or number_of_subscribers:   

        # with a certain probability kill the sub and pub candidates (the right operator can be modified)
        if number_of_subscribers and (random.uniform(0, 100) < 0.00001):
            number_of_subscribers -= 1

            subscriber_candidate = random.choice(pids_subscribers)
            subscriber_handler.kill_subscriber(subscriber_candidate, pids_subscribers) 
            # since it's a simulation of a sub crash, this line should be commented at the final version. The sub process will say "crashed" anyway
            print(f"[main] Killed the Sub with pid {subscriber_candidate}", flush=True)
        
        if number_of_publishers and (random.uniform(0, 100) < 0.00001):
            number_of_publishers -= 1
            
            publisher_candidate = random.choice(pids_publishers)
            publisher_handler.kill_publisher(publisher_candidate, pids_publishers)
            # since it's a simulation of a pub crash, this line should be commented at the final version. The pub process will say "crashed" anyway
            print(f"[main] Killed the Pub with pid {publisher_candidate}", flush=True)

        # time.sleep(0.1)
    
    print("[main] -----------------------------", flush=True)
    print("[main] Simulation completed", flush=True)
    print("[main] -----------------------------\n", flush=True)
