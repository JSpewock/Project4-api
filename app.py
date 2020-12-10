from flask import Flask, jsonify, g, request
from flask_cors import CORS
import os
from functools import wraps
import jwt

import models
from resources.rants import rants
from resources.comments import comments
from resources.users import users

#all information on jwt and creating decorators was taken from https://www.youtube.com/watch?v=WxGBoY5iNXY
def login_check(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None

    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']
    
    if not token:
      return jsonify(data={}, status={"code": 401, "message" : "Login required"})
    
    try:
      data = jwt.decode(token, 'THISISASECRETKEY')
      current_user = models.Users.get(models.Users.id == data['id'])
    except:
      return jsonify(data={}, status={"code": 401, "message": "Token is invalid"})

    return f(current_user, *args, **kwargs)
  return decorated

DEBUG = True
PORT = 8000

app = Flask(__name__)

CORS(rants, origins=['http://localhost:3000', 'https://project-4-client-rantz.herokuapp.com'], supports_credentials=True)
app.register_blueprint(rants, url_prefix='/rantz')

CORS(comments, origins=['http://localhost:3000', 'https://project-4-client-rantz.herokuapp.com'], supports_credentials=True)
app.register_blueprint(comments, url_prefix='/comments')

CORS(users, origins=['http://localhost:3000', 'https://project-4-client-rantz.herokuapp.com'], supports_credentials=True)
app.register_blueprint(users, url_prefix='/users')

@app.before_request
def before_request():
  """Connect to the database before each request."""
  print("you should see this before each request")
  g.db = models.DATABASE
  g.db.connect()

@app.after_request
def after_request(response):
  """Close db after each request"""
  print("you should see this after each request")
  g.db.close()
  return response

@app.route('/')
def index():
  return 'hello'

@app.route('/login')
def login():
  auth = request.authorization
  print(auth)
  return ""


if 'ON_HEROKU' in os.environ:
  print('\non Heorku!')
  models.initialize()

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)