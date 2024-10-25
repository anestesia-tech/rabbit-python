#!/usr/bin/python3
import pika

rabbitmq_host = 'localhost'  # Укажите адрес вашего RabbitMQ сервера
rabbitmq_port = 5672          # Порт по умолчанию
username = 'tech'            # Имя пользователя
password = 'passwd'            # Пароль
vhost = 'main'                # Укажите ваш виртуальный хост

# Создание подключения к RabbitMQ
credentials = pika.PlainCredentials(username, password)
connection_params = pika.ConnectionParameters(host=rabbitmq_host,
                                              port=rabbitmq_port,
                                              virtual_host=vhost,
                                              credentials=credentials)

# Устанавливаем соединение и открываем канал
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Список очередей для чтения сообщений
queues = ['queue1', 'queue2', 'queue3']

def callback(ch, method, properties, body):
    print(f"Получено сообщение из {method.routing_key}: {body.decode()}")

# Подписка на каждую очередь и ожидание сообщений
try:
    for queue in queues:
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        print(f"Ожидание сообщений из очереди: {queue}")

    # Запуск цикла ожидания сообщений
    channel.start_consuming()

except KeyboardInterrupt:
    print("Остановка скрипта.")
finally:
    # Закрытие соединения
    connection.close()
