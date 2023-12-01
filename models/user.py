from db import db

from models.utils import UtilsClass

class UserModel(db.Model, UtilsClass):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), nullable=False)
  password = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  assignedIssues = db.relationship('IssueModel', back_populates='assigneeUser', foreign_keys='IssueModel.assigneeUserId')
  reportedIssues = db.relationship('IssueModel', back_populates='reporterUser', foreign_keys='IssueModel.reporterUserId')
  projectsOwner = db.relationship('ProjectModel', back_populates='owner', foreign_keys='ProjectModel.ownerId')

  projects = db.relationship('ProjectModel', back_populates='team_members', secondary='project_members')
  