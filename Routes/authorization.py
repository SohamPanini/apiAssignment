from functools import wraps
from flask import Flask, jsonify, request, Blueprint
import redis
import jwt
import datetime

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

authorization_bp = Blueprint('authorization', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        else:
            return jsonify({'error': 'Bearer token is malformed!'}), 400

        if redis_client.sismember('revoked_tokens', token):
            return jsonify({'error': 'Token has been revoked!'}), 401

        try:
            data = jwt.decode(token, authorization_bp.config, algorithms=['HS256'])
            print(data)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        return f(data, *args, **kwargs)

    return decorated

@authorization_bp.route('/check_token_status', methods=['GET'])
@token_required
def check_status(data):
    # If the token is valid, this function will be called
    return jsonify({'message': 'Token is valid', 'user_data': data}), 200

@authorization_bp.route('/revoke_token', methods=['POST'])
@token_required
def revoke_token(decoded_token):
    print("this is the decoded token", decoded_token)
    token = request.headers.get('Authorization')
    token = token[7:]
    redis_client.sadd('revoked_tokens', token)
    return jsonify({'message': 'Token has been revoked!'}), 200

@authorization_bp.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.json
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Refresh token is required in the body!'}), 400
    
    try:
        decoded_refresh_token = jwt.decode(refresh_token, authorization_bp.config, algorithms=['HS256'])
        email = decoded_refresh_token['email']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Refresh token has expired! User Logged out!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid refresh token!'}), 401
    
    # Check if the refresh token exists in Redis for the user
    stored_refresh_token = redis_client.get(f'refresh_token:{email}')
    if stored_refresh_token != refresh_token:
        return jsonify({'error': 'Invalid refresh token!'}), 401
    
    new_access_token = jwt.encode({'email': email, 'exp': datetime.datetime.now(datetime.timezone.utc)+ datetime.timedelta(minutes=2)},
                    authorization_bp.config, algorithm='HS256')
    
    return jsonify({'access_token':new_access_token}), 200

@authorization_bp.route('/authorized', methods=['GET'])
@token_required
def authorized_user(decoded_token):
    return jsonify({'message': f'Welcome {decoded_token["email"]}'}), 200