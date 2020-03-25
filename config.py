import os

from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'secret-keys-are-big-secrets-for-now'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'triviabros', 'trivia.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
