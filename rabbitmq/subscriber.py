import pika
import sys
import signal
from time import time

class Subscriber():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGUSR1, self.sigusr1_handler)

        # prepare our subscriber
        self.exchange = sys.argv[1]
        self.id_sub = sys.argv[2]
        self.binding_keys = sys.argv[3:]

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

        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True)

        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        arrival_time = int(time() * 1000) # in ms
        latency = arrival_time - properties.timestamp
        print(f"[sub #{self.id_sub}] Got in {latency}ms :{method.routing_key}:{body}", flush=True)

    def sigterm_handler(self, sig, frame):
        print(f"[sub #{self.id_sub}] Crashed", flush=True)
        # we should close the connection here
        # we should close the queue here as well, but seems that (empirically) is closed from the killing action anyway
        sys.exit(0)

    def sigusr1_handler(self, sig, frame):
        self.channel.stop_consuming()
        self.connection.close()
        print(f"[sub #{self.id_sub}] Exited", flush=True)
        sys.exit(0)

Subscriber()