import pika
import sys
from time import sleep, time
import signal
from numpy import random
from utils import create_topic

class Publisher():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGUSR1, self.sigusr1_handler)

        # prepare our publisher
        self.exchange = sys.argv[1]
        self.id_pub = sys.argv[2]
        self.elapsed = 0
        self.previous_sent = 0

        random.seed(int(self.id_pub))

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

        print(f'[pub #{self.id_pub}] Connected to {self.exchange} exchange', flush=True)

        message = "Hello World! #" + self.id_pub
        self.file = open(f'data{self.id_pub}.txt', 'w')
        
        while not self.elapsed:
            topic = create_topic('publisher')
            sending_time = int(time() * 1000) # in ms
            self.file.write(str(sending_time - self.previous_sent) + '\n')
            self.previous_sent = sending_time
            properties = pika.BasicProperties(timestamp=sending_time)
            channel.basic_publish(exchange=self.exchange, routing_key=topic, body=message, properties=properties)        
            print(f"[pub #{self.id_pub}] Sent {topic}:{message}", flush=True) # [{string_time}]
            sleep(random.exponential(scale=3.0, size=None)/100) # to simulate the random message sending

        
        connection.close()

    def sigterm_handler(self, sig, frame):
        print(f"[pub #{self.id_pub}] Crashed", flush=True)
        # we should close the connection here
        self.file.close()
        sys.exit(0)

    def sigusr1_handler(self, sig, frame):
        self.elapsed = 1
        print(f"[pub #{self.id_pub}] Exited", flush=True)
        self.file.close()

Publisher()