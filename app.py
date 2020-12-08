from flask import Flask

DEBUG = True
PORT = os.environ.PORT or 8000

app = Flask(__name__)

@app.route('/')
def index():
  return 'hello'


if __name__ == '__main__':
  app.run(debug=DEBUG, port=PORT)