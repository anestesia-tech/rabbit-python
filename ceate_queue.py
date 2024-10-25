#!/usr/bin/python3
import pika

rabbitmq_host = 'localhost'
rabbitmq_port = 5672
username = 'tech'
password = 'passwd'
vhost = 'main'

credentials = pika.PlainCredentials(username, password)
connection_params = pika.ConnectionParameters(host=rabbitmq_host,
                                              port=rabbitmq_port,
                                              virtual_host=vhost,
                                              credentials=credentials)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

queues = ['queue1', 'queue2', 'queue3']

for queue in queues:
    channel.queue_declare(queue=queue, durable=True)  # durable=True делает очередь устойчивой к перезагрузке

print("Очереди созданы:", queues)

connection.close()
