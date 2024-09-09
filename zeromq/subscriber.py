import zmq
import sys
import signal
from time import time
from utils import create_topic

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
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(f"tcp://localhost:{self.port}")
        
        if not self.binding_keys:
            sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
            sys.exit(1)

        for binding_key in self.binding_keys:
            self.socket.setsockopt_string(zmq.SUBSCRIBE, binding_key)

        print(f'[sub #{self.id_sub}] Connected to {self.port} port and topics {self.binding_keys}. Waiting for logs', flush=True)

        self.file = open(f'latencies{self.id_sub}.txt', 'w')
        
        while not self.elapsed:
            message = self.socket.recv()
            _, send_time, m = str(message).split(':')
            arrival_time = int(time() * 1000) # in ms
            latency = arrival_time - int(send_time)
            self.file.write(str(latency) + '\n')
            print(f"[sub #{self.id_sub}] Got in {latency}ms: {m}", flush=True)

    def sigterm_handler(self, sig, frame):
        print(f"[sub #{self.id_sub}] Crashed", flush=True)
        self.file.close()
        sys.exit(0)

    def sigusr1_handler(self, sig, frame):
        print(f"[sub #{self.id_sub}] Exited", flush=True)
        self.file.close()
        self.socket.close()
        sys.exit(0)

Subscriber()