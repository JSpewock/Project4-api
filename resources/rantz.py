import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict 

rantz = Blueprint('rantz', 'rant')

@rantz.route('/', methods=["GET"])
def get_all_rants():
  return "hello from the index route"