import pika
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
        self.binding_keys = create_topic('subscriber')

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        if not self.binding_keys:
            sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
            sys.exit(1)

        for binding_key in self.binding_keys:
            self.channel.queue_bind(
                exchange=self.exchange, queue=queue_name, routing_key=binding_key)

        print(f'[sub #{self.id_sub}] Connected to {self.exchange} exchange and topics {self.binding_keys}. Waiting for logs', flush=True)
        
        self.file = open(f'latencies{self.id_sub}.txt', 'w')

        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True)

        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        arrival_time = int(time() * 1000) # in ms
        latency = arrival_time - properties.timestamp
        self.file.write(str(latency) + '\n')
        print(f"[sub #{self.id_sub}] Got in {latency}ms :{method.routing_key}:{body}", flush=True)

    def sigterm_handler(self, sig, frame):
        print(f"[sub #{self.id_sub}] Crashed", flush=True)
        self.file.close()
        sys.exit(0)

    def sigusr1_handler(self, sig, frame):
        self.channel.stop_consuming()
        self.connection.close()
        self.file.close()
        print(f"[sub #{self.id_sub}] Exited", flush=True)
        sys.exit(0)

Subscriber()