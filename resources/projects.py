import logging
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from schemas import ProjectSchema, UpdateProjectSchema, ProjectMemberSchema, IssueSchemaForProject, IssueSchema, CreateIssueInsideProjectSchema
from models.project import ProjectModel
from models.user import UserModel
from models.issue import IssueModel
from db import db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

blp = Blueprint('projects', __name__, description='Operations on projects')

@blp.route('/projects/<string:project_id>')
class projectProject(MethodView):

  # GET PROJECT
  @blp.response(200, ProjectSchema)
  def get(self, project_id):
    '''Get project by id'''
    project = ProjectModel.query.get_or_404(project_id)
    return project

  # DELETE PROJECT METHOD
  def delete(self, project_id):
    '''Delete project by id'''
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
    '''Update project by id'''
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
    '''Return list of all projects'''
    return ProjectModel.query.all()
  
  # CREATE PROJECT METHOD
  @blp.arguments(ProjectSchema)
  @blp.response(201, ProjectSchema)
  def post(self, project_data):
    '''Create new project'''
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
    '''Add user with {user_id} to project with {project_id} as member'''
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
    '''Delete user with {user_id} from project with {project_id} as member'''
    project = ProjectModel.query.get_or_404(project_id)
    user = UserModel.query.get_or_404(user_id)

    project.team_members.remove(user)

    try:
      db.session.add(project)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return {'message': 'User removed from team', 'user': user, 'project': project}
  
@blp.route('/projects/<string:project_id>/issues')
class IssueComments(MethodView):
  @jwt_required()
  @blp.response(200, IssueSchemaForProject(many=True))
  def get(self, project_id):
    '''Return all project issues'''
    project = ProjectModel.query.get_or_404(project_id)

    return project.issues.all()
  
  @blp.arguments(CreateIssueInsideProjectSchema)
  @blp.response(201, IssueSchema)
  def post(self, issue_data, project_id):
    '''Create new issue'''
    project = ProjectModel.query.get_or_404(project_id)
    issue = IssueModel(projectId=project_id, **issue_data)

    project.issues.append(issue)

    try:
      db.session.add(project)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return issue