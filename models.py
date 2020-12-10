from peewee import *
import os
from playhouse.db_url import connect
import datetime
from flask_login import UserMixin

if 'ON_HEROKU' in os.environ:
  DATABASE = connect(os.environ.get('DATABASE_URL'))

else :
  DATABASE = PostgresqlDatabase('rantz')

class Users(UserMixin, Model):
  username = CharField(unique=True)
  password = CharField()

  class Meta:
    database = DATABASE


class Rants(Model):
  title = CharField()
  body = CharField()
  created_by = ForeignKeyField(Users, backref='rants')
  created_at = DateTimeField(default=datetime.datetime.now)

  class Meta:
    database = DATABASE

class Comments(Model):
  # created_by = ForeignKeyField(Users, backref='user_comment')
  body = CharField()
  parent_post = ForeignKeyField(Rants, backref='comments')
  created_at = DateTimeField(default=datetime.datetime.now)

  class Meta:
    database = DATABASE


def initialize():
  DATABASE.connect()
  DATABASE.create_tables([Rants, Users, Comments], safe=True)
  print("tables created")
  DATABASE.close()