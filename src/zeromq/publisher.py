from time import sleep
import zmq
import sys
import signal

class Publisher():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        # Prepare our context and publisher
        context   = zmq.Context(1)
        publisher = context.socket(zmq.PUB)
        publisher.connect(f"tcp://localhost:{sys.argv[1]}")
        print(f'[pub #{sys.argv[2]}] Connected to port:{sys.argv[1]} and topic {sys.argv[3]}', flush=True)
        
        topic = sys.argv[3]

        message = f"'Hello World! #{sys.argv[2]}'"

        while True:
            # Write two messages, each with an envelope and content
            publisher.send_multipart([topic, message])
            print(f"[pub #{sys.argv[2]}] Sent {topic}:{message}", flush=True)
            sleep(1)
        
        # We never get here but clean up anyhow
        publisher.close()
        context.term()

    def sigterm_handler(self, sig, frame):
        print(f"[pub #{sys.argv[2]}] Crashed", flush=True)
        sys.exit(0)

Publisher()