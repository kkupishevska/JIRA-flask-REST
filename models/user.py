from .. import db

from models.utils import UtilsClass

class UserModel(db.Model, UtilsClass):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), nullable=False)
  passwordHash = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  assignedIssues = db.relationship('Issue', back_populates='assigneeUser', lazy='dynamic')
