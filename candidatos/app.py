from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret')


jwt = JWTManager(app)


@app.route('/apply-to-job', methods=['POST'])
@jwt_required()
def applyToJob():
    claims = get_jwt()
    if claims['role'] != 'Candidato':
        return jsonify({"message": "Access forbidden: Candidatos only"}), 403
    return jsonify({"message": "Application registered!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
