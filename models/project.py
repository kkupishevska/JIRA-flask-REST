from db import db

from models.utils import UtilsClass

class ProjectModel(db.Model, UtilsClass):
  __tablename__ = 'project'

  id = db.Column(db.Integer, primary_key=True)
  projectKey = db.Column(db.String(10), nullable=False)
  projectName = db.Column(db.String(255), nullable=False)
  description = db.Column(db.Text)
  createdByUserId = db.Column(db.Integer, db.ForeignKey('user.id'))
  createdByUser = db.relationship('UserModel', foreign_keys=[createdByUserId])
  ownerId = db.Column(db.Integer, db.ForeignKey('user.id'))
  owner = db.relationship('UserModel', foreign_keys=[ownerId])
  team_members = db.relationship('UserModel', secondary='project_members', back_populates='projects')

  issues = db.relationship('IssueModel', back_populates='project', lazy='dynamic', cascade='all, delete')
  