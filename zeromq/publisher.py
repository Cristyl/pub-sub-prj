import zmq
import sys
from time import sleep
import signal

class Publisher():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        # prepare our context and publisher
        port = sys.argv[1]
        topic = sys.argv[3]
        id_pub = sys.argv[2]

        context   = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.connect(f"tcp://localhost:{port}")
        print(f'[pub #{id_pub}] Connected to {port} port and topic {topic}', flush=True)
        
        message = "Hello World! #" + id_pub

        while True:
            socket.send_string(f"{topic}:{message}")
            print(f"[pub #{id_pub}] Sent {topic}:{message}", flush=True)
            sleep(1)
        
        # we never get here but clean up anyhow
        socket.close()
        context.term()

    def sigterm_handler(self, sig, frame):
        print(f"[pub #{sys.argv[2]}] Crashed", flush=True)
        sys.exit(0)

Publisher()