import zmq
import sys
import signal

class Broker():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGUSR1, self.sigusr1_handler)

        self.context = zmq.Context()
        
        # socket facing subscribers
        self.frontend = self.context.socket(zmq.SUB)
        self.frontend.bind(f"tcp://*:{sys.argv[1]}")
        self.frontend.setsockopt(zmq.SUBSCRIBE, b"")
        
        # socket facing publishers
        self.backend  = self.context.socket(zmq.PUB)
        self.backend.bind(f"tcp://*:{sys.argv[2]}")

        self.id = sys.argv[3]
        
        print(f"[Broker #{self.id}] Broker is set up with port {sys.argv[2]} for pubs and port {sys.argv[1]} for subs", flush=True)

        zmq.proxy(self.frontend, self.backend)
        
    def sigterm_handler(self, sig, frame):
        print(f"[Broker] Crashed", flush=True)
        sys.exit(0)
    
    def sigusr1_handler(self, sig, frame):
        print(f"[Broker #{self.id}] Terminated.", flush=True)
        if self.frontend:
            self.frontend.close()
        if self.backend:
            self.backend.close()
        if self.context:
            self.context.term()
        sys.exit(0)
        
Broker()