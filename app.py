from flask import Flask, jsonify, g
import os

import models
from resources.rantz import rantz

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.register_blueprint(rantz, url_prefix='/rantz')

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


if 'ON_HEROKU' in os.environ:
  print('\non Heorku!')
  models.initialize()

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)