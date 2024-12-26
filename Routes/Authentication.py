import datetime
from flask_bcrypt import Bcrypt
import jwt
from flask import Flask, jsonify, request, Blueprint
import redis

auth_bp = Blueprint('app2', __name__)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@auth_bp.route('/')
def home():
    return "Hello, Flask!"

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    if redis_client.hexists('users', email):
        return jsonify({'error': 'User Already exists!'}), 409
    
    password_hash = auth_bp.bcrypt.generate_password_hash(password).decode('utf-8')

    redis_client.hset('users',email,password_hash)
    return jsonify({'message': 'User created successfully!'}), 201

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required!'}), 400

    hashed_password = redis_client.hget('users', email)
    if not hashed_password or not auth_bp.bcrypt.check_password_hash(hashed_password, password):
        return jsonify({'error': 'Invalid credentials!'}), 401
    
    token = jwt.encode({'email': email, 'exp': (datetime.datetime.now(datetime.timezone.utc)) + datetime.timedelta(minutes=1)},
                       auth_bp.config, algorithm='HS256')
    return jsonify({'token': token}), 200