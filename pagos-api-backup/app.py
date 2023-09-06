from flask import Flask

app = Flask(__name__)

@app.route('/')
def pagoNomina():
    return 'Pago hecho desde instancia pagos-backup!', 200
    
@app.route('/health')
def healthcheck():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
