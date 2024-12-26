import datetime
from flask_bcrypt import Bcrypt
import jwt
from flask import Flask, jsonify, request, Blueprint
import redis

authentication_bp = Blueprint('authentication', __name__)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@authentication_bp.route('/')
def home():
    return "Hello, Flask!"

@authentication_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    if redis_client.hexists('users', email):
        return jsonify({'error': 'User Already exists!'}), 409
    
    password_hash = authentication_bp.bcrypt.generate_password_hash(password).decode('utf-8')

    redis_client.hset('users',email,password_hash)
    return jsonify({'message': 'User created successfully!'}), 201

@authentication_bp.route('/signin', methods=['POST'])
def signin():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required!'}), 400
    
    if not redis_client.hexists('users', email):
        return jsonify({'error': 'User does not exist'}), 404

    hashed_password = redis_client.hget('users', email)
    if not hashed_password or not authentication_bp.bcrypt.check_password_hash(hashed_password, password):
        return jsonify({'error': 'Invalid credentials!'}), 401
    
    acccess_token = jwt.encode({'email': email, 'exp': datetime.datetime.now(datetime.timezone.utc)+ datetime.timedelta(minutes=2),
                                'token_type': 'access'},
                       authentication_bp.config, algorithm='HS256')
    
    refresh_token = jwt.encode({'email': email, 'exp': datetime.datetime.now(datetime.timezone.utc)+ datetime.timedelta(minutes=5),
                                'token_type': 'refresh'},
                        authentication_bp.config, algorithm='HS256')
    
    redis_client.set(f'refresh_token:{email}', refresh_token)

    return jsonify({'access_token': acccess_token, 'refresh_token': refresh_token}), 200