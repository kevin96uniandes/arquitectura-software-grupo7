import requests, time, pika, json
from datetime import datetime  

def enviarNotificacion(mensaje):
    connection  = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
    channel = connection.channel()
    channel.queue_declare(queue='notificaciones')
    channel.basic_publish(exchange='', routing_key='notificaciones', body=mensaje)
    connection.close()
    print("Mensaje enviado: " + mensaje)

def monitor():
    url_pagos_1 = "http://pagos-1:5000/healthcheck"
    url_pagos_2 = "http://pagos-2:5000/healthcheck"
    url_candidatos = "http://candidatos:5000/healthcheck"
    while (True):
        response1 = requests.get(url_pagos_1)
        if response1.status_code != 200:
            mensaje = {"instance":"pagos-1", "status":"Servicio no disponible", "timestamp":datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
            enviarNotificacion(json.dumps(mensaje))
           
        response2 = requests.get(url_pagos_2)
        if response2.status_code != 200:
            mensaje = {"instance":"pagos-2", "status":"Servicio no disponible", "timestamp":datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
            enviarNotificacion(json.dumps(mensaje))
            
        response3 = requests.get(url_candidatos)
        if response3.status_code != 200:
            mensaje = {"instance":"candidatos", "status":"Servicio no disponible", "timestamp":datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
            enviarNotificacion(json.dumps(mensaje))
            
        time.sleep(3)

if __name__ == '__main__':
    monitor()
