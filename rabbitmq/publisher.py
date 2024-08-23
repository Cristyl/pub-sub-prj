import pika
import sys
from time import sleep
import signal
from random import randint
from utils import create_topic

class Publisher():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=sys.argv[1], exchange_type='topic')

        # Question: Is it better the random crash in here or in the main?
        print(f'[pub #{sys.argv[2]}] Connected to {sys.argv[1]} exchange', flush=True)
        message = f"'Hello World! #{sys.argv[2]}'"
        
        while True:
            topic = create_topic('publisher')
            channel.basic_publish(exchange=sys.argv[1], routing_key=topic, body=message)        
            print(f"[pub #{sys.argv[2]}] Sent {topic}:{message}", flush=True)
            # messages_to_send -= 1
            sleep(randint(1, 5))

        connection.close()

    def sigterm_handler(self, sig, frame):
        print(f"[pub #{sys.argv[2]}] Crashed", flush=True)
        sys.exit(0)

Publisher()