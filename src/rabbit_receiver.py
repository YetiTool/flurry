#!/usr/bin/env python
import pika


### INITIALISE RABBITMQ

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='machine_status_1')


### INTIALISE LOCAL DB

localDBClient = None

port = 8086  # default port
user = "rabbit_receiver"  # the user/password created for the pi, with write access
password = "up9Rn0U9GMR5TJix" 
dbname = "machine_data"  # the database we created earlier
interval = 5  # Sample period in seconds

try:
    # Ansible may not have pre-installed this
    from influxdb import InfluxDBClient # database lib
    localDBClient = InfluxDBClient("localhost", port, user, password, dbname)
    print "Connected to local db"

except:
    print "Unable to initialise local database. Have libs been installed? Or check DatabaseStorage credentials?"


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# EXAMPLE MSG: time:2020-07-22 14:58:49.234871|machineID:test_local|spindle_on_off:1
    
    msg_elements = body.split("|")
    
    for pair in msg_elements:
        if pair.startswith('time'):
            time = pair.split(";")[1]
        elif pair.startswith('machineID'):
            machineID = pair.split(";")[1]
        else:
            name = pair.split(";")[0]
            value = pair.split(";")[1]

    data = [
        {
            "measurement": machineID,
            "tags": {
                "source": "rabbit_receiver",
            },
            "time": time,
            "fields": {
                name: float(value)
            }
        }
    ]
        
    # Send the JSON data to InfluxDB
    if localDBClient != None: 
        try:
            print data    
            localDBClient.write_points(data)
            print "Written to db OK:"
        except:
            print "Failed to write to db."
    else:
        print "Did not attempt to write to db: client was not initialised."


channel.basic_consume(
    queue='machine_status_1', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()