import sys
import random
from time import time, sleep
from utils import *
import os
import matplotlib.pyplot as plt

random.seed(42)
            
if __name__ == "__main__":
    # define the number of publishers and subscribers (it can modify the upper and lower bounds)
    if len(sys.argv) != 3 or sys.argv[1].isdigit() == False or sys.argv[2].isdigit() == False or int(sys.argv[1]) > CONST.MAX_PUB and int(sys.argv[2]) > sys.argv[2]:
        print(f"[main] Usage: python3 main.py <num_of_pub> <num_of_sub> (the values of the parameters must be at max respectively {CONST.MAX_PUB}, {CONST.MAX_SUB})", flush=True)
        sys.exit(1)

    number_of_publishers  = int(sys.argv[1])
    number_of_subscribers = int(sys.argv[2])
    next_pub_id = number_of_publishers
    next_sub_id = number_of_subscribers

    start_time = time()
    print("\n[main] -----------------------------", flush=True)
    print("[main] Simulation start", flush=True)
    print("[main] -----------------------------", flush=True)

    # create the broker first of all
    create_broker()
    sleep(1) # to wait for the broker to be ready

    # create the subscribers
    for subscriber_id in range(number_of_subscribers):
        create_node(CONST.PUBS_PORT, subscriber_id, 'subscriber')

    # create the publishers
    # [we create first the subscribers to not risk to loose any message]
    for publisher_id in range(number_of_publishers):
        create_node(CONST.SUBS_PORT, publisher_id, 'publisher')

    elapsed = 0

    # stay into the while loop till there is a pub or a sub
    while number_of_publishers or number_of_subscribers:
        # with a certain probability kill the sub and pub candidates (the right operator can be modified)
        if number_of_subscribers and (random.uniform(0, 100) < CONST.KILL_PROBABILITY):
            candidate = random.choice(subscriber_handler.pids)
            if candidate is not None:
                number_of_subscribers -= 1
                delete_node(candidate, 'subscriber')

        if number_of_publishers and (random.uniform(0, 100) < CONST.KILL_PROBABILITY):
            candidate = random.choice(publisher_handler.pids)
            if candidate is not None:
                number_of_publishers -= 1
                delete_node(candidate, 'publisher')

        # randomly create a new publisher
        if random.uniform(0, 100) < CONST.CREATION_PROBABILIY and number_of_publishers <= CONST.MAX_PUB:
            create_node(CONST.SUBS_PORT, next_pub_id, 'publisher')
            print(f"[main] Pub #{next_pub_id} has joined", flush=True)
            number_of_publishers += 1
            next_pub_id += 1

        # randomly create a new subscriber      
        if random.uniform(0, 100) < CONST.CREATION_PROBABILIY and number_of_subscribers <= CONST.MAX_SUB:
            create_node(CONST.PUBS_PORT, next_sub_id, 'subscriber')
            print(f"[main] Sub #{next_sub_id} has joined", flush=True)
            number_of_subscribers += 1
            next_sub_id += 1

        # end the simulation after a certain time
        if time() - start_time >= CONST.MAX_DURATION:

            elapsed = 1

            for subscriber in subscriber_handler.pids:
                if subscriber is not None:
                    delete_node(subscriber, 'subscriber')
                    number_of_subscribers -= 1

            for publisher in publisher_handler.pids:
                if publisher is not None:
                    delete_node(publisher, 'publisher')
                    number_of_publishers -= 1
            
            delete_broker()

    sleep(1) # to wait for all the processes to finish their work
    if (elapsed):
        print("[main] The maximum execution time (" + str(CONST.MAX_DURATION) + "s) has expired", flush=True)
        print("[main] The simulation is about to terminate", flush=True)
        sleep(1) # only for a GUI motivation

    print("[main] -----------------------------", flush=True)
    print("[main] Simulation completed", flush=True)
    print("[main] -----------------------------\n", flush=True)

    sleep(2) # only for a GUI motivation
    print("Performing the distribution...", flush=True)

    data = []
    for i in range(next_pub_id):
        f = open(f"data{i}.txt", "r")
        lines = f.readlines()
        for line in lines:
            data.append(int(line.strip()))
        f.close()
        if os.path.exists(f'data{i}.txt'):
            os.remove(f'data{i}.txt')
    
    # data to plot
    data.sort()
    data = data[:-next_pub_id]
    print(data)

    # create histogram
    plt.hist(data)
    
    # display histogram
    plt.show()