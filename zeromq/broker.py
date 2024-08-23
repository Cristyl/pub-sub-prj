import zmq
import sys
import signal

class Broker():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        context = zmq.Context()
        
        # socket facing subscribers
        frontend = context.socket(zmq.SUB)
        frontend.bind(f"tcp://*:{sys.argv[1]}")
        frontend.setsockopt(zmq.SUBSCRIBE, b"")
        
        # socket facing publishers
        backend  = context.socket(zmq.PUB)
        backend.bind(f"tcp://*:{sys.argv[2]}")
        
        print(f"[Broker] Broker is set up with port {sys.argv[1]} for pubs and port {sys.argv[2]} for subs", flush=True)

        zmq.proxy(frontend, backend)
        
        # we never get here…
        frontend.close()
        backend.close()
        context.term()
        
    def sigterm_handler(self, sig, frame):
        print(f"[Broker] Crashed", flush=True)
        sys.exit(0)
        
Broker()