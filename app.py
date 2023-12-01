import os
from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
import models 
from resources.hello import blp as HelloBlp
from resources.projects import blp as ProjectsBlp
from resources.users import blp as UsersBlp
from resources.issues import blp as IssuesBlp
from resources.comments import blp as CommentsBlp

from config import config

migrate = Migrate()

def create_app():
  app = Flask(__name__)
  app.config.from_object(config[os.getenv('CONFIG_MODE')])

  db.init_app(app)
  migrate.init_app(app, db)
  jwt = JWTManager(app)

  api = Api(app)
  api.register_blueprint(HelloBlp)
  api.register_blueprint(ProjectsBlp)
  api.register_blueprint(UsersBlp)
  api.register_blueprint(IssuesBlp)
  api.register_blueprint(CommentsBlp)

  return app
