import sys
import random
from time import time, sleep
from utils import *

random.seed(42)
            
if __name__ == "__main__":
    # define the number of publishers and subscribers (it can modify the upper and lower bounds)
    if len(sys.argv) != 3 or sys.argv[1].isdigit() == False or sys.argv[2].isdigit() == False:
        print("[main] Usage: python3 main.py <num_of_pub> <num_of_sub>", flush=True)
        sys.exit(1)

    number_of_publishers  = int(sys.argv[1])
    number_of_subscribers = int(sys.argv[2])
    next_pub_id = number_of_publishers
    next_sub_id = number_of_subscribers

    # list of the exchanges
    exchange_names = CONST.EXCHANGE_NAMES

    start_time = time()
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

    elapsed = 0

    # stay into the while loop till there is a pub or a sub
    while number_of_publishers or number_of_subscribers:
        # with a certain probability kill the sub and pub candidates (the right operator can be modified)
        if number_of_subscribers and (random.uniform(0, 100) < CONST.KILL_PROBABILITY):
            number_of_subscribers -= 1
            delete_node(random.choice(subscriber_handler.pids), 'subscriber')

        if number_of_publishers and (random.uniform(0, 100) < CONST.KILL_PROBABILITY):
            number_of_publishers -= 1
            delete_node(random.choice(publisher_handler.pids), 'publisher')

        # randomly create a new publisher
        if random.uniform(0, 100) < CONST.CREATION_PROBABILIY:
            create_node(exchange_names, next_pub_id, 'publisher')
            print(f"[main] Pub #{next_pub_id} has joined", flush=True)
            next_pub_id += 1
            number_of_publishers += 1

        # randomly create a new subscriber      
        if random.uniform(0, 100) < CONST.CREATION_PROBABILIY:
            create_node(exchange_names, next_sub_id, 'subscriber')
            print(f"[main] Sub #{next_sub_id} has joined", flush=True)
            number_of_subscribers += 1
            next_sub_id += 1

        # end the simulation after a certain time
        if time() - start_time >= CONST.MAX_DURATION:

            elapsed = 1

            for subscriber in subscriber_handler.pids:
                delete_node(subscriber, 'subscriber')
                number_of_subscribers -= 1

            for publisher in publisher_handler.pids:
                delete_node(publisher, 'publisher')
                number_of_publishers -= 1

    if (elapsed):
        sleep(1)
        print("[main] The maximum execution time (60s) has expired")
        print("[main] The simulation is about to terminate")
        sleep(1)

    print("[main] -----------------------------", flush=True)
    print("[main] Simulation completed", flush=True)
    print("[main] -----------------------------\n", flush=True)