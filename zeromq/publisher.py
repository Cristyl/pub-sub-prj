import zmq
import sys
from time import sleep
import signal
import random
from utils import create_topic



class Publisher():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGUSR1, self.sigusr1_handler)

        # prepare our context and publisher
        self.port = sys.argv[1]
        self.id_pub = sys.argv[2]
        self.elapsed = 0

        random.seed(self.id_pub)

        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.connect(f"tcp://localhost:{self.port}")
        
        print(f'[pub #{self.id_pub}] Connected to {self.port} port', flush=True)
        
        message = "Hello World! #" + self.id_pub

        while not self.elapsed:
            topic = create_topic('publisher')
            socket.send_string(f"{topic}:{message}")
            print(f"[pub #{self.id_pub}] Sent {topic}:{message}", flush=True)
            sleep(random.uniform(1, 5)) # to simulate the random message sending
        
        socket.close()
        context.term()

    def sigterm_handler(self, sig, frame):
        print(f"[pub #{self.id_pub}] Crashed", flush=True)
        sys.exit(0)
    
    def sigusr1_handler(self, sig, frame):
        self.elapsed = 1
        print(f"[pub #{self.id_pub}] Exited", flush=True)

Publisher()