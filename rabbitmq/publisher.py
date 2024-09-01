import pika
import sys
from time import sleep
import signal
import random
from utils import create_topic

class Publisher():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        # prepare our publisher
        self.exchange = sys.argv[1]
        self.id_pub = sys.argv[2]

        random.seed(self.id_pub)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

        print(f'[pub #{self.id_pub}] Connected to {self.exchange} exchange', flush=True)

        message = "Hello World! #" + self.id_pub
        
        while True:
            topic = create_topic('publisher')
            channel.basic_publish(exchange=self.exchange, routing_key=topic, body=message)        
            print(f"[pub #{self.id_pub}] Sent {topic}:{message}", flush=True)
            sleep(random.uniform(1, 5)) # to simulate the random message sending

        # we never get here but close anyhow
        connection.close()

    def sigterm_handler(self, sig, frame):
        print(f"[pub #{self.id_pub}] Crashed", flush=True)
        sys.exit(0)

Publisher()