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
    parser.add_option("--user", default="guest:guest",
                      help="rabbitmq user")
    parser.add_option("--msg", default="hello-world",
                      help="message to send")
    parser.add_option("--num", default=1000000,
                      help="How many messages to send")
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

    for x in range (0, int(options.num)):
        chan2.basic_publish(exchange=options.exchange,
                      routing_key=queue_name,
                      body=str(options.msg + '-%i' % (x)))
        print(" [x] Sent " + options.msg + '-%i' % (x))
        #time.sleep(1) #If some wait time is needed between publish threads

    conn1.close()
    conn2.close()

if __name__ == "__main__":
    exit(main())
