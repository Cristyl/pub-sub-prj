import pika
import sys
import time
import signal

class Publisher():
    def __init__(self):
        # setup signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=sys.argv[1], exchange_type='topic')

        # Question: Is it better the random crash in here or in the main?
        print(f'[pub #{sys.argv[2]}] Connected to {sys.argv[1]} exchange and topic {sys.argv[3]}', flush=True)
        routing_key = sys.argv[3]
        message = f"'Hello World! #{sys.argv[2]}'"
        
        # messages_to_send = 5
        while True:
            channel.basic_publish(exchange=sys.argv[1], routing_key=routing_key, body=message)        
            print(f"[pub #{sys.argv[2]}] Sent {routing_key}:{message}", flush=True)
            # messages_to_send -= 1
            time.sleep(1)

        connection.close()

    def sigterm_handler():
        print(f"[pub #{sys.argv[2]}] Crashed", flush=True)
        sys.exit(0)

Publisher()