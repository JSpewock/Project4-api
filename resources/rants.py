import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict 

rants = Blueprint('rantz', 'rant', url_prefix='rantz')

#index
@rants.route('/', methods=["GET"])
def get_all_rants():
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
  print(rant.__dict__)
  return jsonify(data=model_to_dict(rant), status={"code": 200, "message": "success"})