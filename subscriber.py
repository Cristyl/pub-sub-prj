#!/usr/bin/env python
import pika
import sys

class Subscriber():
    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=sys.argv[1], exchange_type='fanout')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=sys.argv[1], queue=queue_name)

        print(' [*] Waiting for logs. To exit press CTRL+C')
        print(f'Hi I am receiver {sys.argv[2]}, I am connected to exchange {sys.argv[1]}')

        def callback(ch, method, properties, body):
            print(f" [x] I, receiver {sys.argv[2]}, got {body}")

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

Subscriber()