from db import db

from models.utils import UtilsClass

class UserModel(db.Model, UtilsClass):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), nullable=False)
  password = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  # assignedIssues = db.relationship('IssueModel', back_populates='assigneeUser', lazy='dynamic')
