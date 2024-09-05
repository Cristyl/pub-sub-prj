import zmq
import sys
import signal
from utils import create_topic
from time import time

class Subscriber():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGUSR1, self.sigusr1_handler)
    
        # prepare our context and subscriber
        self.port = sys.argv[1]
        self.id_sub = sys.argv[2]
        self.binding_keys = create_topic('subscriber')
        self.elapsed = 0

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://localhost:{self.port}")
        
        if not self.binding_keys:
            sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
            sys.exit(1)

        for binding_key in self.binding_keys:
            socket.setsockopt_string(zmq.SUBSCRIBE, binding_key)

        print(f'[sub #{self.id_sub}] Connected to {self.port} port and topics {self.binding_keys}. Waiting for logs', flush=True)
        
        while not self.elapsed:
            message = socket.recv()
            arrival_time = int(time() * 1000) # in ms
            latency = arrival_time - message.split(":")[0]

            print(f"[sub #{self.id_sub}] Got in {latency}ms :{message}", flush=True)
            self.old_arrival_time = arrival_time

        socket.close()
        context.term()

    def sigterm_handler(self, sig, frame):
        print(f"[sub #{self.id_sub}] Crashed", flush=True)
        # we should close the socket and the context here
        sys.exit(0)

    def sigusr1_handler(self, sig, frame):
        self.elapsed = 1
        print(f"[sub #{self.id_sub}] Exited", flush=True)
        sys.exit(0)

Subscriber()