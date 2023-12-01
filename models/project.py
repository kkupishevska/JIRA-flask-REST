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
