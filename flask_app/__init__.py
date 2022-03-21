from flask import Flask
from flask_app.env import Key
app = Flask(__name__)

app.secret_key=Key