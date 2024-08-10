import pika
import sys
import time
import signal

class Publisher():
    def __init__(self):
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=sys.argv[1], exchange_type='fanout')

        # Question: Is it better the random crash in here or in the main?
        print(f'[pub #{sys.argv[2]}] Connected to {sys.argv[1]} exchange', flush=True)

        message = f"'Hello World! #{sys.argv[2]}'"
        
        messages_to_send = 5
        while True:
            channel.basic_publish(exchange=sys.argv[1], routing_key='', body=message)        
            print(f"[pub #{sys.argv[2]}] Sent {message}", flush=True)
            messages_to_send -= 1
            time.sleep(1)

        connection.close()

    def sigterm_handler(self, signum, frame):
        print(f"[pub #{sys.argv[2]}] Crashed", flush=True)
        sys.exit(0)
    

Publisher()