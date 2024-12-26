from flask import Flask
from flask_bcrypt import Bcrypt
import redis
import datetime
from Routes.Authentication import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TEST'


bcrypt = Bcrypt(app) 
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

auth_bp.bcrypt = bcrypt
auth_bp.config = app.config['SECRET_KEY']
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True,port=8080)