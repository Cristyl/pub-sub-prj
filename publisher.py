#!/usr/bin/env python
import pika
import sys

class Publisher():
    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs1', exchange_type='fanout')

        message = ' '.join(sys.argv[1:]) or "info: Hello World!"
        channel.basic_publish(exchange='logs1', routing_key='', body=message)
        print(f" [x] Sent {message}")
        connection.close()
        
Publisher()