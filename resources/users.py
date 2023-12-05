from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from db import db

from models import UserModel
from schemas import UpdateUserSchema, UserSchema, LoginSchema, PlainUserSchema

blp = Blueprint('Users', __name__, description='Operations with users')

@blp.route('/register')
class UserRegister(MethodView):
  @blp.arguments(PlainUserSchema)
  def post(self, user_data):
    '''Register new user'''
    if UserModel.query.filter(UserModel.email == user_data['email']).first():
      abort(409, message='A user with that email already exists.')

    user = UserModel(**user_data)
    user.password = pbkdf2_sha256.hash(user_data['password'])

    try:
      db.session.add(user)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return {'message': 'User successfuly created.'}, 201
  
@blp.route('/login')
class UserLogin(MethodView):
  @blp.arguments(LoginSchema)
  def post(self, login_data):
    '''Login method: returns token'''
    user = UserModel.query.filter(UserModel.email == login_data['email']).first()
    if user and pbkdf2_sha256.verify(login_data['password'], user.password):
      identity = {
        'id': user.id, 
        'email': user.email, 
        # 'role': user.role if user.role else 'user'
        }
      access_token = create_access_token(identity=identity)
      return {'token': access_token}

    abort(404, message='A user with such email and password does not exist.')


@blp.route('/users')
class UsersList(MethodView):
  @blp.response(200, UserSchema(many=True))
  def get(self):
    '''Get all users'''
    return UserModel.query.all()
  

@blp.route('/users/<int:user_id>')
class UserItem(MethodView):

  @blp.response(200, UserSchema)
  def get(self, user_id):
    '''Get user information by id'''
    return UserModel.query.get_or_404(user_id)
  
  @blp.arguments(UpdateUserSchema)
  @blp.response(200, UserSchema)
  def put(self, user_data, user_id):
    '''Edit user information'''
    if user := UserModel.query.get_or_404(user_id):
      user.update_attributes(**user_data)
    else: user = UserModel(id=user_id, **user_data)

    try:
      db.session.add(user)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return user
  
  def delete(self, user_id):
    '''Delete user'''
    user = UserModel.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return {'message': 'User is successfuly deleted'}, 200