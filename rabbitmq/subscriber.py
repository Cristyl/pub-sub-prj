import pika
import pika.exceptions
import sys
import signal
from time import time
from utils import CONST, create_topic

class Subscriber():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGUSR1, self.sigusr1_handler)

        # prepare our subscriber
        self.exchange = CONST.EXCHANGE_NAME
        self.id_sub = sys.argv[1]
        self.binding_keys = (create_topic('subscriber')).split(" ")
        self.ports = [5672, 5673, 5674]
        self.connection = None
        self.channel = None
        self.dict = {}
        self.lost_messages = 0

        self.file = open(f'latencies{self.id_sub}.txt', 'w')
        
        #setup connection to the cluster of rabbitmq nodes
        self.connect_to_cluster()

    def connect_to_cluster(self):
        # attempt to connect to any available node in the cluster
        for port in self.ports:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host='localhost', port=port)
                )
                self.channel = self.connection.channel()
                self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')
                
                result = self.channel.queue_declare(queue='', exclusive=True)
                queue_name = result.method.queue

                if not self.binding_keys:
                    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
                    sys.exit(1)

                for binding_key in self.binding_keys:
                    self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=binding_key)

                self.channel.basic_consume(
                    queue=queue_name, on_message_callback=self.callback, auto_ack=True
                )

                print(f'[sub #{self.id_sub}] Connected to RabbitMQ on port {port} and with topics {self.binding_keys}. Waiting for logs', flush=True)
                self.channel.start_consuming()
            except pika.exceptions.AMQPConnectionError:
                print(f"[sub #{self.id_sub}] Failed to connect on port {port}, trying next...", flush=True)
                continue
        else:
            raise Exception(f"[sub #{self.id_sub}] Unable to connect to any cluster node.")

    def callback(self, ch, method, properties, body):
        # callback to process incoming messages and calculate latency
        try:
            arrival_time = int(time() * 1000)  # in ms
            latency = arrival_time - properties.timestamp
            self.file.write(str(latency) + '\n')
            message, id_pub, topic, counter = body.decode('utf-8').split(':')
            counter = int(counter)        
            print(f"[sub #{self.id_sub}] Got in {latency}ms: {topic}:{message}", flush=True)
            expected_message = self.dict.get((id_pub, topic), 0)
            if expected_message != counter - 1 and expected_message != 0:
                print(f"[sub #{self.id_sub}] Lost a message", flush=True)
                self.lost_messages += counter - expected_message
            self.dict[(id_pub, topic)] = counter

        except pika.exceptions.AMQPConnectionError:
            print(f"[sub #{self.id_sub}] Connection lost during message processing, reconnecting...", flush=True)
            self.connect_to_cluster()

    def sigterm_handler(self, sig, frame):
        print(f"[sub #{self.id_sub}] Crashed", flush=True)
        with open(f'mess_lost{self.id_sub}.txt', 'w') as f:
            f.write(str(self.lost_messages))
        if self.file:
            self.file.close()
        if self.connection and self.connection.is_open:
            self.connection.close()
        sys.exit(0)

    def sigusr1_handler(self, sig, frame):
        self.channel.stop_consuming()
        if self.connection and self.connection.is_open:
            self.connection.close()
        if self.file:
            self.file.close()
        print(f"[sub #{self.id_sub}] Exited", flush=True)
        with open(f'mess_lost{self.id_sub}.txt', 'w') as f:
            f.write(str(self.lost_messages))
        sys.exit(0)

Subscriber()
