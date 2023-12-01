import logging
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from schemas import IssueSchema, UpdateIssueSchema, CommentSchema, PlainIssueCommentSchema
from models.issue import IssueModel
from models.comment import CommentModel
from db import db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

blp = Blueprint('Issues', __name__, description='Operations on issues')

@blp.route('/issues/<string:issue_id>')
class Issue(MethodView):

  # GET ISSUE
  @blp.response(200, IssueSchema)
  def get(self, issue_id):
    issue = IssueModel.query.get_or_404(issue_id)
    return issue

  # DELETE ISSUE METHOD
  def delete(self, issue_id):
    # jwt = get_jwt()
    # if not jwt.get('is_admin'):
    #   abort(401, message='Blah-blah, no roots')
    issue = IssueModel.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    
    return {'message': 'Issue deleted'}, 200
  
  @blp.arguments(UpdateIssueSchema)
  @blp.response(200, IssueSchema)
  def put(self, issue_data, issue_id):
    logger.debug(f"Received issue_data in put method: {issue_data} {type(issue_data)}")
    if (issue := IssueModel.query.get_or_404(issue_id)):
      issue.update_attributes(**issue_data)
    else: issue = IssueModel(id=issue_id, **issue_data)

    logger.debug(f"{issue} {type(issue)}")

    try:
      db.session.add(issue)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, message="Error occurred")

    return issue

@blp.route('/issues')
class IssuesList(MethodView):

  # GET ISSUES LIST
  @blp.response(200, IssueSchema(many=True))
  def get(self):
    return IssueModel.query.all()
  
  # CREATE ISSUE METHOD
  @blp.arguments(IssueSchema)
  @blp.response(201, IssueSchema)
  def post(self, issue_data):
    issue = IssueModel(**issue_data)

    try:
      db.session.add(issue)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return issue
  
@blp.route('/issue/<string:issue_id>/comments')
class IssueComments(MethodView):
  @blp.response(200, CommentSchema(many=True))
  def get(self, issue_id):
    issue = IssueModel.query.get_or_404(issue_id)

    return issue.comments.all()
  
  @blp.arguments(PlainIssueCommentSchema)
  @blp.response(201, CommentSchema)
  def post(self, comment_data, issue_id):
    comment = CommentModel(**comment_data, issueId=issue_id)

    try:
      db.session.add(comment)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return comment