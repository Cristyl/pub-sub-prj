import sys
import random
from time import time, sleep
from utils import *
import matplotlib.pyplot as plt
import os

#seed the random number generator for reproducibility
random.seed(42)
            
if __name__ == "__main__":
    # define the number of publishers and subscribers (it can modify the upper and lower bounds)
    if len(sys.argv) != 3 or sys.argv[1].isdigit() == False or sys.argv[2].isdigit() == False or int(sys.argv[1]) > CONST.MAX_PUB and int(sys.argv[2]) > sys.argv[2]:
        print(f"[main] Usage: python3 main.py <num_of_pub> <num_of_sub> (the values of the parameters must be at max respectively {CONST.MAX_PUB}, {CONST.MAX_SUB})", flush=True)
        sys.exit(1)

    number_of_publishers  = int(sys.argv[1])
    number_of_subscribers = int(sys.argv[2])
    number_of_brokers = CONST.NUMBER_OF_BROKERS
    next_pub_id = number_of_publishers
    next_sub_id = number_of_subscribers

    start_time = time()
    print("\n[main] -----------------------------", flush=True)
    print("[main] Simulation start", flush=True)
    print("[main] -----------------------------", flush=True)

    # create the broker first of all
    for broker_id in range(number_of_brokers):
        create_broker(broker_id)
    sleep(1) # to wait for the broker to be ready

    # create the subscribers
    for subscriber_id in range(number_of_subscribers):
        create_node(subscriber_id, 'subscriber')

    # create the publishers
    # [we create first the subscribers to not risk to loose any message]
    for publisher_id in range(number_of_publishers):
        create_node(publisher_id, 'publisher')

    #variables for loop ending
    elapsed = 0
    flag = False

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
            create_node(next_pub_id, 'publisher')
            print(f"[main] Pub #{next_pub_id} has joined", flush=True)
            number_of_publishers += 1
            next_pub_id += 1

        # randomly create a new subscriber      
        if random.uniform(0, 100) < CONST.CREATION_PROBABILIY and number_of_subscribers <= CONST.MAX_SUB:
            create_node(next_sub_id, 'subscriber')
            print(f"[main] Sub #{next_sub_id} has joined", flush=True)
            number_of_subscribers += 1
            next_sub_id += 1

        # condition checker for broker closure
        # used mostly to see how the system reacts if one or more brokers are closed
        # the timing, the pid and the number of closed brokers can be modified
        if time() - start_time >= 15 and flag:
            delete_broker(broker_handler.pids[0])
            print(f"[main] Closed the first broker", flush=True)
            flag = False
            sleep(0.1)
            delete_broker(broker_handler.pids[1])
            print(f"[main] Closed the second broker", flush=True)

        # end the simulation after a certain time
        if time() - start_time >= CONST.MAX_DURATION:

            elapsed = 1

            for subscriber in subscriber_handler.pids:
                if subscriber is not None:
                    delete_node(subscriber, 'subscriber', termination=True)
                    number_of_subscribers -= 1

            for publisher in publisher_handler.pids:
                if publisher is not None:
                    delete_node(publisher, 'publisher', termination=True)
                    number_of_publishers -= 1

            for broker in broker_handler.pids:
                if broker is not None:
                    delete_broker(broker, terminated=True)

    sleep(1) # to wait for all the processes to finish their work
    if (elapsed):
        print("[main] The maximum execution time (" + str(CONST.MAX_DURATION) + "s) has expired", flush=True)
        print("[main] The simulation is about to terminate", flush=True)
        sleep(1) # only for a GUI motivation

    print("[main] -----------------------------", flush=True)
    print("[main] Simulation completed", flush=True)
    print("[main] -----------------------------\n", flush=True)

    sleep(2) # only for a GUI motivation
    print("Performing the measures...", flush=True)

    # collect inter arrival times
    inter_arrival_times = []
    for i in range(next_pub_id):
        f = open(f"inter{i}.txt", "r")
        lines = f.readlines()
        for line in lines:
            inter_arrival_times.append(int(line.strip()))
        f.close()
        if os.path.exists(f'inter{i}.txt'):
            os.remove(f'inter{i}.txt')
    
    inter_arrival_times.sort()
    inter_arrival_times = inter_arrival_times[:-next_pub_id]
    
    num_bins = 10
    bin_size = inter_arrival_times[-1] / num_bins
    bin_labels = []
    bin_data = []
    next = 0
    for i in range(num_bins):
        x1 = round((i*0.1) + next, 2)
        x2 = round(x1 + bin_size, 2)
        bin_labels.append(f"{x1}-{x2}")
        next += bin_size
        bin_data.append(0)

    for time in inter_arrival_times:
        for i in range(num_bins):
            interval = bin_labels[i].split("-")
            if(time >= float(interval[0]) and time <= float(interval[1])):
                bin_data[i] += 1
                break

    # collect number of arrivals
    number_of_arrivals = [0 for _ in range(next_pub_id)]
    for i in range(next_pub_id):
        f = open(f"counter{i}.txt", "r")
        line = f.readline()
        number_of_arrivals[i] = int(line)
        f.close()
        if os.path.exists(f'counter{i}.txt'):
            os.remove(f'counter{i}.txt')
    
    # print(f"Bin labels: {bin_labels}", flush=True)
    # print(f"Bin data: {bin_data}", flush=True)
    # print(f'Number of arrivals: {number_of_arrivals}')
    
    # collect latencies
    completions = [0 for _ in range(next_sub_id)]
    latencies   = [0 for _ in range(next_sub_id)]
    for i in range(next_sub_id): #number_of_subscribers?
        latencies_cont = 0
        f = open(f"latencies{i}.txt", "r")
        lines = f.readlines()
        f.close()
        
        for line in lines:
            latencies[i] += int(line.strip())
            latencies_cont += 1
        if latencies_cont != 0:
            latencies[i] /= latencies_cont
        completions[i] = latencies_cont
        
        if os.path.exists(f'latencies{i}.txt'):
            os.remove(f'latencies{i}.txt')

    latencies.sort()

    # print(f"Latencies: {latencies}", flush=True)
    
    # collect number of messages lost by every subscriber
    lost_messages = []
    for i in range(next_sub_id):
        f = open(f"mess_lost{i}.txt", "r")
        lost_messages.append(int(f.read()))
        f.close()
        if os.path.exists(f"mess_lost{i}.txt"):
            os.remove(f"mess_lost{i}.txt")
    
    # workload parameters and performance measures (taken wrt a time interval T) 
    T = CONST.MAX_DURATION      # system observation interval
    A = sum(number_of_arrivals) # num of arrivals
    C = sum(completions)        # num of completions
    l = A / T                   # arrival rate
    X = C / T                   # throughput
    B = T                       # busy period of time
    U = B / T                   # (resource) utilization (law)
    S = B / C                   # average service time per completion
    
    print("-----------Information obtained by the simulation-------------------------")
    print(f"System observation interval: {T}s", flush=True)
    
    print("Number of arrivals: ", sum(number_of_arrivals), flush=True)
    print(f"Mean latency of the system: {sum(latencies) / len(latencies)}ms",flush=True)
    
    print("Number of completions: ", sum(completions),flush=True)
    print("Lost messages: ", sum(lost_messages), flush=True)
    print(f"Arrival rate: {l} msgs/s",flush=True)
    print(f"Throughput: {X} completions/s", flush=True)
    print(f"Busy period of time: ~{B}ms", flush=True)
    print(f"Resource utilization: ~{U}ms", flush=True)
    print(f"Average service time per completion: {S}ms", flush=True)
    print("-------------------------------------------------------------------------")

    # create histograms over all the collected data and print other information
    pub_labels = [f'pub{i}' for i in range(next_pub_id)]
    # print(f"Pub labels: {pub_labels}", flush=True)
    sub_labels = [f'sub{i}' for i in range(next_sub_id)]
    # print(f"Sub labels: {sub_labels}", flush=True)

    fig = plt.figure()
    fig.suptitle('Workload plotting (using ZeroMQ)')
    gs = fig.add_gridspec(2,2)
    
    ax1 = fig.add_subplot(gs[1, :])
    ax1.bar(bin_labels, bin_data)
    ax1.set_xlabel('Milliseconds (ms)\nInter-arrival times (estimation of the PDF)')
    ax1.set_ylabel('#occurrences per bin')
    
    ax2 = fig.add_subplot(gs[0, 0])
    ax2.bar(pub_labels, number_of_arrivals)
    ax2.set_xlabel('Number of arrivals per pub')
    ax2.set_ylabel('#messages')
    
    ax3 = fig.add_subplot(gs[0, 1])
    ax3.bar(sub_labels, latencies)
    ax3.set_xlabel('Mean latencies per pub')
    ax3.set_ylabel('Milliseconds (ms)')
    
    # display histogram
    plt.show()