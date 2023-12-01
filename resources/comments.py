import logging
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from schemas import CommentSchema, UpdateCommentSchema
from models.comment import CommentModel
from models.user import UserModel
from db import db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

blp = Blueprint('Comments', __name__, description='Operations on comments')

@blp.route('/comments/<string:comment_id>')
class commentComment(MethodView):
  # DELETE COMMENT METHOD
  def delete(self, comment_id):
    comment = CommentModel.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    
    return {'message': 'Comment deleted'}, 200
  
  @blp.arguments(UpdateCommentSchema)
  @blp.response(200, CommentSchema)
  def put(self, comment_data, comment_id):
    logger.debug(f"Received comment_data in put method: {comment_data} {type(comment_data)}")
    if (comment := CommentModel.query.get_or_404(comment_id)):
      comment.update_attributes(**comment_data)
    else: comment = CommentModel(id=comment_id, **comment_data)

    logger.debug(f"{comment} {type(comment)}")

    try:
      db.session.add(comment)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, message="Error occurred")

    return comment

@blp.route('/comments')
class commentList(MethodView):

  # GET COMMENTS LIST
  @blp.response(200, CommentSchema(many=True))
  def get(self):
    return CommentModel.query.all()
  
  # CREATE COMMENT METHOD
  @blp.arguments(CommentSchema)
  @blp.response(201, CommentSchema)
  def post(self, comment_data):
    comment = CommentModel(**comment_data)

    try:
      db.session.add(comment)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, message="Error occurred")

    return comment
