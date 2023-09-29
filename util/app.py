from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate
import json
import os
from flask import Response


app = Flask(__name__)


with open('key.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=b'experimento',
        backend=default_backend()
    )
    
   
with open('cert.pem', 'rb') as cert_file:
    cert_data = load_pem_x509_certificate(cert_file.read(), backend=default_backend())
    public_key = cert_data.public_key()
    
    
def encrypt_data(data):
    ciphertext = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def decrypt_data(ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()
    

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    string_data = json.dumps(data)
    encrypted_string_data = encrypt_data(string_data)
    return jsonify({'encData': encrypted_string_data.hex()})


@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_string_data = bytes.fromhex(request.json.get('encData'))
    string_data = decrypt_data(encrypted_string_data)
    data = json.loads(string_data)
    return data
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
