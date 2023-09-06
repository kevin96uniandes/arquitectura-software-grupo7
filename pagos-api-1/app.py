from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def pagoNomina():
    return 'Pago hecho desde instancia pagos-1!', 200
    
@app.route('/health')
def healthcheck():
    response = requests.get("http://mockserver:8080/mock1/health")
    return '', response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
