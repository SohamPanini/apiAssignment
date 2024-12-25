from flask_bcrypt import Bcrypt 
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash

app = Flask(__name__)
bcrypt = Bcrypt(app) 

users = {}

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    if email in users:
        return jsonify({'error': 'User Already exists!'}), 409
    
    users[email] = bcrypt.generate_password_hash(password).decode('utf-8')
    return jsonify({'message': 'User created successfully!'}), 201

@app.route('/signup', methods=['GET'])
def signupValue():
    return jsonify({'users':users}), 200

if __name__ == '__main__':
    app.run(debug=True,port=8080)