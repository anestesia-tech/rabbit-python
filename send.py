#!/usr/bin/python3
import pika
import json
import time

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

#queues = ['queue1', 'queue2', 'queue3']
queues = ['test3-queue']
try:
    for i in range(12000000000):
        message = {
            'message_id': i,
            'content': f'Hello from message {i}',
            'timestamp': time.time()
        }

        for queue in queues:
            channel.basic_publish(exchange='',
                                  routing_key=queue,
                                  body=json.dumps(message),
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,  # Устойчивое сообщение
                                  ))
            print(f"Отправлено сообщение в {queue}: {message}")

        time.sleep(1)  # Задержка в 1 секунду между сообщениями

except Exception as e:
    print("Ошибка при отправке сообщений:", e)

finally:
    # Закрытие соединения
    connection.close()
