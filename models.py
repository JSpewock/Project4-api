from peewee import *
import os
from playhouse.db_url import connect
import datetime

if 'ON_HEROKU' in os.environ:
  DATABASE = connect(os.environ.get('DATABASE_URL'))

else :
  DATABASE = PostgresqlDatabase('rantz')



class Rant(Model):
  title = CharField()
  body = CharField()
  created_at = DateTimeField(default=datetime.datetime.now)

  class Meta:
    database = DATABASE


def initialize():
  DATABASE.connect()
  DATABASE.create_tables([Rant], safe=True)
  print("tables created")
  DATABASE.close()