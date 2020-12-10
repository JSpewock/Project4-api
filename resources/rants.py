import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from functools import wraps
import jwt

# from app import login_check

rants = Blueprint('rantz', 'rant', url_prefix='rantz')

# token_required = login_check

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
      return jsonify(data={}, status={"code": 401, "message": "Token has expired"})

    return f(current_user, *args, **kwargs)
  return decorated

# ------------------------------------
#               Rants
# ------------------------------------

#index
@rants.route('/', methods=["GET"])
@login_check
def get_all_rants(current_user):
  try:
    rants = [model_to_dict(rant) for rant in models.Rants.select()]
    print(rants)
    return jsonify(data=rants, status={"code": 200, "message": "success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "error getting the data"})

#create
@rants.route('/', methods=["POST"])
def create_rant():
  payload = request.get_json()
  print(payload)
  new_rant = models.Rants.create(**payload)
  rant_dict = model_to_dict(new_rant)
  return jsonify(data=rant_dict, status={"code": 200, "message": "success"})

#show
@rants.route('/<id>', methods=["GET"])
def get_one_rant(id):
  rant = models.Rants.get_by_id(id)
  rant_dict = model_to_dict(rant)
  comments = [model_to_dict(comment) for comment in rant.comments]
  post = {"post": rant_dict, "comments": comments}
  return jsonify(data=post, status={"code": 200, "message": "success"})

#update
@rants.route('/<id>', methods=["PUT"])
def update_rant(id):
  payload = request.get_json()
  query = models.Rants.update(**payload).where(models.Rants.id == id)
  query.execute()
  return jsonify(data=model_to_dict(models.Rants.get_by_id(id)), status={"code": 200, "message": "success"})

#delete
@rants.route('/<id>', methods=["DELETE"])
def delete_rant(id):
  rant = models.Rants.get_by_id(id)
  rant_dict = model_to_dict(rant)
  print(rant_dict)
  query = models.Rants.delete().where(models.Rants.id == id)
  query.execute()
  return jsonify(data=rant_dict, status={"code": 200, "message": "success, deleted"})
