import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from db import db
import models
import schemas

from resources.projects import blp as ProjectsBlp
from resources.users import blp as UsersBlp
from resources.issues import blp as IssuesBlp
from resources.comments import blp as CommentsBlp

from config import config

migrate = Migrate()

def create_app():
  app = Flask(__name__)
  app.config.from_object(config[os.getenv('CONFIG_MODE')])
  CORS(app)

  db.init_app(app)
  migrate.init_app(app, db)
  jwt = JWTManager(app)

  @jwt.additional_claims_loader
  def add_claims_to_jwt(identity):
    # if identity['role'] == 'admin':
    if identity['id'] == 1:
      return {'is_admin': True}
    return {'is_admin': False}

  @jwt.expired_token_loader
  def expired_token_callback(error, jwt_payload):
    return (
      jsonify(
      {'message': 'The token has expired.', 'error': 'token_expired'}),
      401
    )
  
  @jwt.invalid_token_loader
  def invalid_token_callback(error):
    return (
      jsonify(
      {'message': 'Signature verification failed.', 'error': 'invalid_token'}),
      401
    )
  
  @jwt.unauthorized_loader
  def missing_token_callback(error):
    return (
      jsonify(
        {'message': 'Request doesnt contain an access token.', 'error': 'authorization_required'}
      ), 401
    )

  api = Api(app)

  api.register_blueprint(ProjectsBlp)
  api.register_blueprint(UsersBlp)
  api.register_blueprint(IssuesBlp)
  api.register_blueprint(CommentsBlp)

  return app
