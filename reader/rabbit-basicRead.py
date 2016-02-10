#!/usr/bin/env python
# coding: latin-1
from __future__ import print_function

import time
import optparse
import pika

target_queue='testqueue'

def main():
    parser = optparse.OptionParser()
    parser.add_option("--host", default="localhost",
                      help="rabbitmq host")
    parser.add_option("-x", "--exchange", default="entry",
                      help="exchange to publish to")
    parser.add_option("-k", "--routing-key", default="#",
                      help="routing key")
    parser.add_option("-t", "--type", default="topic",
                      help="exchange type")
    parser.add_option("--user", default="admin",
                      help="rabbitmq user")
    parser.add_option("--passwd", default="mypass",
                      help="rabbitmq password")
    (options, args) = parser.parse_args()

    conn1 = pika.BlockingConnection(
        pika.URLParameters("amqp://" + options.user + ":" + options.passwd +"@@localmachineIPaddr@:5672/%2F"))
    chan1 = conn1.channel()
    chan1.exchange_declare(
        exchange=options.exchange, type=options.type)

    conn2 = pika.BlockingConnection(
        pika.URLParameters("amqp://" + options.user + ":" + options.passwd +"@@localmachineIPaddr@:5672/%2F"))
    chan2 = conn2.channel()
    result = chan2.queue_declare(queue=target_queue, auto_delete=True)
    queue_name = result.method.queue

    chan2.queue_bind(exchange=options.exchange,
        queue=queue_name, routing_key=options.routing_key)

    print(' [*] Connected to Host: '+ options.host)
    print(' [*] Connected to Exchange: ' + options.exchange)
    print(' [*] Connected to Queue: ' + queue_name)

    #read a message from the queue, then publish it back to the queue
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        #time.sleep(1)

    chan2.basic_consume(callback, queue=queue_name, no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    chan2.start_consuming()

if __name__ == "__main__":
    exit(main())
