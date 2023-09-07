from flask import Flask
import requests

app = Flask(__name__)

@app.route('/crear-candidato', methods=['POST'])
def crearCandidato():
    return 'Candidato creado!', 200
    
@app.route('/healthcheck')
def healthcheck():
    response = requests.get("http://mockserver:8080/mock3/health")
    return '', response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
