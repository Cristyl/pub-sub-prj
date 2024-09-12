import zmq
import sys
from time import sleep, time
import signal
from numpy import random
from utils import create_topic, CONST



class Publisher():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGUSR1, self.sigusr1_handler)

        # prepare our context and publisher
        self.ports = CONST.PUBS_PORT
        self.id_pub = sys.argv[1]
        self.elapsed = 0
        self.previous_sent = 0
        self.counter = 0
        self.dict = {}

        random.seed(int(self.id_pub))

        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        for port in self.ports:
            socket.connect(f"tcp://localhost:{port}")
        
        print(f'[pub #{self.id_pub}] Connected to {self.ports} ports', flush=True)
        
        message = "Hello World! #" + self.id_pub
        
        self.file = open(f'inter{self.id_pub}.txt', 'w')

        while not self.elapsed:
            topic = create_topic('publisher')
            sending_time = int(time() * 1000) # in ms
            self.file.write(str(sending_time - self.previous_sent) + '\n')
            self.previous_sent = sending_time
            id_message = self.dict.get(topic, 0)
            socket.send_string(f"{topic}:{sending_time}:{message}:{self.id_pub}:{id_message}")
            if id_message == 0:
                self.dict[topic] = 1
            else:
                self.dict[topic] += 1
            self.counter += 1
            print(f"[pub #{self.id_pub}] Sent {topic}:{message}", flush=True)
            sleep(random.exponential(scale=3.0, size=None)/100) # to simulate the random message sending
        socket.close()
        context.term()

    def sigterm_handler(self, sig, frame):
        print(f"[pub #{self.id_pub}] Crashed", flush=True)
        self.file.close()
        with open(f'counter{self.id_pub}.txt', 'w') as f:
            f.write(str(self.counter))
        sys.exit(0)
    
    def sigusr1_handler(self, sig, frame):
        self.elapsed = 1
        print(f"[pub #{self.id_pub}] Exited", flush=True)
        self.file.close()
        with open(f'counter{self.id_pub}.txt', 'w') as f:
            f.write(str(self.counter))
        sys.exit(0)

Publisher()