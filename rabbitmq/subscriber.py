import pika
import sys
import signal

class Subscriber():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        self.exchange = sys.argv[1]
        self.id_sub = sys.argv[2]
        self.binding_keys = sys.argv[3:]

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        
        if not self.binding_keys:
            sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
            sys.exit(1)

        for binding_key in self.binding_keys:
            channel.queue_bind(
                exchange=self.exchange, queue=queue_name, routing_key=binding_key)

        print(f'[sub #{self.id_sub}] Connected to {self.exchange} exchange and topics {self.binding_keys}. Waiting for logs', flush=True)

        def callback(ch, method, properties, body):
            print(f"[sub #{self.id_sub}] Got {method.routing_key}:{body}", flush=True)

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

    def sigterm_handler(self, sig, frame):
        print(f"[sub #{self.id_sub}] Crashed", flush=True)
        sys.exit(0)

Subscriber()