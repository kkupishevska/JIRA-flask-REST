import logging
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from schemas import ProjectSchema, UpdateProjectSchema, ProjectMemberSchema
from models.project import ProjectModel
from models.user import UserModel
from db import db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

blp = Blueprint('projects', __name__, description='Operations on projects')

@blp.route('/projects/<string:project_id>')
class projectProject(MethodView):

  # GET PROJECT
  @blp.response(200, ProjectSchema)
  def get(self, project_id):
    project = ProjectModel.query.get_or_404(project_id)
    return project

  # DELETE PROJECT METHOD
  def delete(self, project_id):
    # jwt = get_jwt()
    # if not jwt.get('is_admin'):
    #   abort(401, message='Blah-blah, no roots')
    project = ProjectModel.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    
    return {'message': 'Project deleted'}, 200
  
  @blp.arguments(UpdateProjectSchema)
  @blp.response(200, ProjectSchema)
  def put(self, project_data, project_id):
    logger.debug(f"Received project_data in put method: {project_data} {type(project_data)}")
    if (project := ProjectModel.query.get_or_404(project_id)):
      project.update_attributes(**project_data)
    else: project = ProjectModel(id=project_id, **project_data)

    logger.debug(f"{project} {type(project)}")

    try:
      db.session.add(project)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, message="Error occurred")

    return project

@blp.route('/projects')
class projectList(MethodView):

  # GET PROJECTS LIST
  @blp.response(200, ProjectSchema(many=True))
  def get(self):
    return ProjectModel.query.all()
  
  # CREATE PROJECT METHOD
  @blp.arguments(ProjectSchema)
  @blp.response(201, ProjectSchema)
  def post(self, project_data):
    project = ProjectModel(**project_data)

    try:
      db.session.add(project)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, message="Error occurred")

    return project
  
@blp.route('/projects/<string:project_id>/user/<string:user_id>')
class LinkProjectsAndMembers(MethodView):
  @blp.response(201, ProjectSchema)
  def post(self, project_id, user_id):
    project = ProjectModel.query.get_or_404(project_id)
    user = UserModel.query.get_or_404(user_id)

    project.team_members.append(user)

    try:
      db.session.add(project)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return project
  
  @blp.response(200, ProjectMemberSchema)
  def delete(self, project_id, user_id):
    project = ProjectModel.query.get_or_404(project_id)
    user = UserModel.query.get_or_404(user_id)

    project.team_members.remove(user)

    try:
      db.session.add(project)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return {'message': 'User removed from team', 'user': user, 'project': project}