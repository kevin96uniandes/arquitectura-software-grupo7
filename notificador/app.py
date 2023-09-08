import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
channel = connection.channel()
channel.queue_declare(queue='notificaciones')
def recibirNotificacion(channel, method, properties, body):
    print("Mensaje recibido: %s" % body)
channel.basic_consume(on_message_callback=recibirNotificacion, queue='notificaciones', auto_ack=True)
print('Esperando mensajes...')
channel.start_consuming()