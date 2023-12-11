from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])
@app.route("/")
@limiter.limit("10/minute") # maximum of 10 requests per minute
def index():
  return "Welcome to my Flask API"





app = Flask(__name__)