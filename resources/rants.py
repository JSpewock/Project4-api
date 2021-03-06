import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from functools import wraps
import jwt

# from app import login_check

rants = Blueprint('rantz', 'rant', url_prefix='rantz')

# token_required = login_check

#all information on jwt and creating decorators was taken from https://www.youtube.com/watch?v=WxGBoY5iNXY
#all information about how to sort and query properly comes from the peewee documentation, http://docs.peewee-orm.com/en/latest/peewee/querying.html#bulk-inserts
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
      current_user = model_to_dict(current_user)
    except:
      return jsonify(data={}, status={"code": 401, "message": "Token is invalid"})

    return f(current_user, *args, **kwargs)
  return decorated

# ------------------------------------
#               Rants
# ------------------------------------

#index
@rants.route('/', methods=["GET"])
def get_all_rants():
  try:
    rants = [model_to_dict(rant) for rant in models.Rants.select().limit(3)]
    print(rants)
    return jsonify(data=rants, status={"code": 200, "message": "success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "error getting the data"})

#create
@rants.route('/', methods=["POST"])
@login_check
def create_rant(current_user):
  payload = request.get_json()
  
  new_rant = models.Rants.create(title=payload['title'], body=payload['body'], topic=payload['topic'], created_by=current_user['id'])
  rant_dict = model_to_dict(new_rant)
  #hide the user who created the posts password
  del rant_dict['created_by']['password']

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
@login_check
def update_rant(current_user, id):
  payload = request.get_json()
  query = models.Rants.update(**payload).where(models.Rants.id == id)
  query.execute()
  return jsonify(data=model_to_dict(models.Rants.get_by_id(id)), status={"code": 200, "message": "success"})

#delete
@rants.route('/<id>', methods=["DELETE"])
@login_check
def delete_rant(current_user, id):
  rant = models.Rants.get_by_id(id)
  rant_dict = model_to_dict(rant)
  print(rant_dict)
  query1 = models.Comments.delete().where(models.Comments.parent_post == id)
  query = models.Rants.delete().where(models.Rants.id == id)
  query1.execute()
  query.execute()
  return jsonify(data=rant_dict, status={"code": 200, "message": "success, deleted"})

#Show User posts
@rants.route('/myposts', methods=["GET"])
@login_check
def user_posts(current_user):
  user = models.Users.get_by_id(current_user['id'])
  posts = [model_to_dict(post) for post in user.rants]
  return jsonify(data=posts, status={"code": 200, "message": "user posts success"})

#sort route
@rants.route('/sort/<topic>', methods=["GET"])
def testing(topic):
  posts = ''
  if topic == 'recent':
    posts_query = models.Rants.select().order_by(-models.Rants.created_at).limit(10)
    posts = [model_to_dict(post) for post in posts_query]
  elif topic == 'all':
    posts_query = models.Rants.select()
    posts = [model_to_dict(post) for post in posts_query]
  else: 
    testing = models.Rants.select().where(models.Rants.topic == topic)
    posts = [model_to_dict(post) for post in testing]
    print(posts)
  # posts = [model_to_dict(post) for post in models.Rants.select('id' == 2)]
  return jsonify(data=posts, status={"code": 200, "message": "successfully filtered"})


