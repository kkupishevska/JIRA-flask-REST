from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api

from .resources.hello import blp as HelloBlp
from .config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_mode):
  app = Flask(__name__)
  app.config.from_object(config[config_mode])

  api = Api(app)

  api.register_blueprint(HelloBlp)

  db.init_app(app)
  migrate.init_app(app, db)

  return app
