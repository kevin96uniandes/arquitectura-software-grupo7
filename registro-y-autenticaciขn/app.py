from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate
import json
import os
import pickle
from flask import Response


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db/experiment.sqlite'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret')


db = SQLAlchemy(app)
jwt = JWTManager(app)


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


@app.before_request
def decrypt_request():
    encrypted_string_data = bytes.fromhex(request.json.get('encData'))
    string_data = decrypt_data(encrypted_string_data)
    data = json.loads(string_data)
    request.data = data
        

def encrypt_response(f):
    def decorated_function(*args, **kwargs):
        result = f(*args, **kwargs)
        resp, status = result
        data = resp
        string_data = data
        encrypted_string_data = encrypt_data(string_data)
        new_resp = jsonify(encData=encrypted_string_data.hex())
        return new_resp, status
    return decorated_function


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    
    
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password",)
        include_relationships = True
        load_instance = True


user_schema = UserSchema()


@app.route('/sign-up', methods=['POST'])
@encrypt_response
def signUp():
    data = request.data
    
    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        return jsonify({'message': 'Invalid data!'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])

    db.session.add(new_user)
    db.session.commit()
    return user_schema.dumps(new_user), 201


@app.route('/sign-in', methods=['POST'])
def signIn():
    data = request.data

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid data!'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Bad credentials!'}), 401

    access_token = create_access_token(identity=user.username, additional_claims={'role': user.role})
    return jsonify(access_token=access_token), 200
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
