import zmq
import sys
import signal

class Broker():
    def __init__(self):
        
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        context = zmq.Context(1)
        
        # Socket facing clients
        frontend = context.socket(zmq.ROUTER)
        frontend.bind(f"tcp://*:{sys.argv[3]}")
        
        # Socket facing services
        backend  = context.socket(zmq.DEALER)
        backend.bind(f"tcp://*:{sys.argv[2]}")
        
        zmq.device(zmq.QUEUE, frontend, backend)
        print(f"[Broker] Broker is set up with port {sys.argv[2]} for pubs and port {sys.argv[3]} for subs", flush=True)
        
        # We never get here…
        frontend.close()
        backend.close()
        context.term()
        
    def sigterm_handler(self, sig, frame):
        print(f"[Broker] Crashed", flush=True)
        sys.exit(0)
        
Broker()