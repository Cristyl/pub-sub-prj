import pika
import pika.exceptions
import sys
from time import sleep, time
import signal
from numpy import random
from utils import create_topic, CONST

class Publisher():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGUSR1, self.sigusr1_handler)

        # prepare our publisher
        self.id_pub = sys.argv[1]
        self.exchange = CONST.EXCHANGE_NAME
        self.elapsed = 0
        self.previous_sent = 0
        self.counter = 0
        self.ports = [5672, 5673, 5674]
        self.dict = {}
        self.connection = None
        self.channel = None

        random.seed(int(self.id_pub))

        #setup connection to the cluster of rabbitmq nodes
        self.connect_to_cluster()

        print(f'[pub #{self.id_pub}] Connected to {self.exchange} exchange', flush=True)

        self.file = open(f'inter{self.id_pub}.txt', 'w')

        while not self.elapsed:
            try:
                self.publish_message()
            except pika.exceptions.AMQPConnectionError:
                print(f"[pub #{self.id_pub}] Connection failed, attempting to reconnect...", flush=True)
                self.connect_to_cluster()
            sleep(random.exponential(scale=3.0, size=None)/100)
        if self.connection and self.connection.is_open:
            self.connection.close()

    def connect_to_cluster(self):
        # attempt to connect to any available node in the cluster
        for port in self.ports:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host='localhost', port=port)
                )
                self.channel = self.connection.channel()
                self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')
                print(f'[pub #{self.id_pub}] Connected to RabbitMQ on port {port}', flush=True)
                break
            except pika.exceptions.AMQPConnectionError:
                print(f"[pub #{self.id_pub}] Failed to connect on port {port}, trying next...", flush=True)
                continue
        else:
            raise Exception(f"[pub #{self.id_pub}] Unable to connect to any cluster node.")

    def publish_message(self):
        # publish a message and handle any disconnection
        topic = create_topic('publisher')
        sending_time = int(time() * 1000)  # in ms
        self.file.write(str(sending_time - self.previous_sent) + '\n')
        self.previous_sent = sending_time
        properties = pika.BasicProperties(timestamp=sending_time)
        id_message = self.dict.get(topic, 0)
        self.channel.basic_publish(exchange=self.exchange, routing_key=topic, body=f"Hello World!:#{self.id_pub}:{topic}:{id_message}", properties=properties)
        if id_message == 0:
                self.dict[topic] = 1
        else:
            self.dict[topic] += 1
        self.counter += 1
        print(f"[pub #{self.id_pub}] Sent {topic}: Hello World! #{self.id_pub}", flush=True)

    def sigterm_handler(self, sig, frame):
        print(f"[pub #{self.id_pub}] Crashed", flush=True)
        self.file.close()
        with open(f'counter{self.id_pub}.txt', 'w') as f:
            f.write(str(self.counter))
        sys.exit(0)

    def sigusr1_handler(self, sig, frame):
        self.elapsed = 1
        print(f"[pub #{self.id_pub}] Exited", flush=True)
        self.file.close()
        with open(f'counter{self.id_pub}.txt', 'w') as f:
            f.write(str(self.counter))
        sys.exit(0)

Publisher()
