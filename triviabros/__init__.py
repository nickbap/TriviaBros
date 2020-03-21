from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-keys-are-big-secrets-for-now'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trivia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

from triviabros import routes