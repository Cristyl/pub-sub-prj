import zmq
import sys
import signal
from utils import create_topic

class Subscriber():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)
    
        # prepare our context and subscriber
        self.port = sys.argv[1]
        self.id_sub = sys.argv[2]

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://localhost:{self.port}")

        binding_keys = create_topic('subscriber')
        
        if not binding_keys:
            sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
            sys.exit(1)

        for binding_key in binding_keys:
            socket.setsockopt_string(zmq.SUBSCRIBE, binding_key)

        print(f'[sub #{self.id_sub}] Connected to {self.port} port and topics {binding_keys}. Waiting for logs', flush=True)
        
        while True:
            message = socket.recv()
            print(f"[sub #{self.id_sub}] Got {message}", flush=True)
 
        # we never get here but clean up anyhow
        socket.close()
        context.term()

    def sigterm_handler(self, sig, frame):
        print(f"[sub #{self.id_sub}] Crashed", flush=True)
        sys.exit(0)

Subscriber()