from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

db = SQLAlchemy()
api = Api(title='FLASK', version='1.0')


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    api.init_app(app)
    db.init_app(app)
    return app
