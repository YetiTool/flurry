#!/usr/bin/env python
import pika
import datetime


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='machine_status_1')

machine_id = 'test_local'
name = 'spindle_on_off'
value = 1

message = "time:" + datetime.datetime.now() + "|machineID:" + machine_id + "|" + name + ":" + str(value)

channel.basic_publish(exchange='', routing_key='machine_status_1', body=message)
print(" [x] Sent:" + message)
connection.close()