#!/usr/bin/env python
import os
import sys
import time
import pika
import json
from subprocess import call

amqp_host = os.environ.get('AMQP_VPN_HOST', 'localhost')
openvpn_exit = call(["openvpn", "--daemon", "--config", "connect.ovpn"])

if openvpn_exit == 0:
    time.sleep(60)
else:
    call(['curl', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', '{"value1": "OpenVPN error"}', os.environ.get('MAKER_ENDPOINT', 'http://localhost/')])

ping_exit = call(["ping", "-c", "3", amqp_host])

if ping_exit != 0:
    amqp_host = os.environ.get('AMQP_PUBLIC_HOST', 'localhost')
    call(['curl', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', '{"value1":"VPN network is not ready"}', os.environ.get('MAKER_ENDPOINT', 'http://localhost/')])
try:
    credit = pika.credentials.PlainCredentials(os.environ.get('AMQP_USERNAME', 'guest'),
        os.environ.get('AMQP_PASSWORD', 'guest'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=amqp_host,
        port=int(os.environ.get('AMQP_PORT', 5672)),
        virtual_host=os.environ.get('AMQP_VHOST', '/'),
        credentials=credit,
        ssl=bool(os.environ.get('AMQP_SSL', False))))
    channel = connection.channel()
    channel.basic_publish(exchange='',routing_key='test',body='test')
    print("Success send message to %s" % (amqp_host))
    connection.close()
except:
    call(['curl', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', '{"value1":"Unable to send message"}', os.environ.get('MAKER_ENDPOINT', 'http://localhost/')])

