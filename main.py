from flask import Flask
from flask_bcrypt import Bcrypt
import redis
from Routes.Authentication import authentication_bp
from Routes.authorization import authorization_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TEST'


bcrypt = Bcrypt(app) 
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

authentication_bp.bcrypt = bcrypt
authentication_bp.config = app.config['SECRET_KEY']
app.register_blueprint(authentication_bp)

authorization_bp.config = app.config['SECRET_KEY']
app.register_blueprint(authorization_bp)

if __name__ == '__main__':
    app.run(debug=True,port=8080)