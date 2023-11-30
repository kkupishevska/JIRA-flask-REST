from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint('Hello', __name__, description='Hello route')

@blp.route('/hello')
class HelloWorld(MethodView):
  def get(self):
    return 'Hello'