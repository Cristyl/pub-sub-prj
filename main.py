# main.py
#!/usr/bin/env python

import sys
from subscriber_handler import Subscriberhandler
import random
import time

'''
def thread_task():
    emit()
'''
random.seed(42)

if __name__ == "__main__":
    #define the number of receivers, can modify the upper and lower bound
    #Todo: the same for publishers
    #Suggestion: put the number of pub/sub as argv
    number_of_subscribers = random.randint(1, 20)

    #define the names of the exchanges, can be modified
    #Todo: put this in a config file
    exchange_names = ['logs1', 'logs2', 'log3', 'logs4']

    #list of the pids of subscribers
    #Todo: the same for publishers
    pids_subscribers = []

    #create the subscriber handler
    #Todo: the same for publishers
    subscriber_handler = Subscriberhandler(number_of_subscribers, exchange_names)

    #create the subscribers
    for subscriber_id in range(number_of_subscribers):
        #choose a name for the exchange of the subscriber
        exchange_name = random.choice(exchange_names)

        #define the command to create the subscriber with id 'subscriber_id'
        command = f'python subscriber.py {exchange_name} {subscriber_id}'

        #create the subscriber
        subscriber_handler.create_subscriber(command, pids_subscribers)

    #create the publishers [we create first the subscribers to not risk to loose any message]

    #killing loop, the condition of the while MUST be modified
    #ERROR the while loop kills all the processes and tries to kill more then existing going in crash of the main
    #must add a condition counter but must be seen the behaviour with both pub/sub
    while True:
        time.sleep(5)
        #choose a candidate to kill
        subscriber_candidate = random.choice(pids_subscribers)

        #with a certain probability kill the candidate, the right operator can be modified
        if random.uniform(0, 100) < 0.001:
            subscriber_handler.kill_subscriber(subscriber_candidate)
            print("Killed a subscriber")
        
        #do the same with the publishers
    '''
    # requests from the command line how many emitters you want
    if len(sys.argv) != 2 or sys.argv[1].isdigit() == False:
        print("[main] Usage: python3 main.py <number_of_emitters>")
        sys.exit(1)

    num_threads = int(sys.argv[1])

    threads = []

    # create and start the emitters (threads)
    for i in range(num_threads):
        thread = threading.Thread(target=thread_task)
        threads.append(thread)
        thread.start()

    # wait for all emitters (threads) to complete
    for thread in threads:
        thread.join()

    print("[main] All emitters have been completed.\n")
'''