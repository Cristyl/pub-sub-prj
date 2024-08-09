import pika
import sys
import signal

class Subscriber():
    def __init__(self):
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=sys.argv[1], exchange_type='fanout')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=sys.argv[1], queue=queue_name)

        print(f'[sub #{sys.argv[2]}] Connected to {sys.argv[1]} exchange. Waiting for logs', flush=True)

        def callback(ch, method, properties, body):
            print(f"[sub #{sys.argv[2]}] Got {body}", flush=True)

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

    def sigterm_handler(self, signum, frame):
        print(f"[sub #{sys.argv[2]}] Crashed", flush=True)
        sys.exit(0)

Subscriber()