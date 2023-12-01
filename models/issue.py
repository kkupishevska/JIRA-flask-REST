from db import db

from models.utils import UtilsClass

class IssueModel(db.Model, UtilsClass):
  __tablename__ = 'issue'

  id = db.Column(db.Integer, primary_key=True)
  projectId = db.Column(db.Integer, db.ForeignKey('project.id'))
  issueKey = db.Column(db.String(15), nullable=False)
  summary = db.Column(db.String(255), nullable=False)
  description = db.Column(db.Text)
  issueType = db.Column(db.String(50), nullable=False)
  status = db.Column(db.String(50), nullable=False)
  priority = db.Column(db.String(50), nullable=False)
  reporterUserId = db.Column(db.Integer, db.ForeignKey('user.id'))
  assigneeUserId = db.Column(db.Integer, db.ForeignKey('user.id'))
  createdDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
  updatedDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
  reporterUser = db.relationship('UserModel', foreign_keys=[reporterUserId], back_populates='reportedIssues')
  assigneeUser = db.relationship('UserModel', foreign_keys=[assigneeUserId], back_populates='assignedIssues')
  # assigneeUser = db.relationship('UserModel', back_populates='assignedIssues')

  comments = db.relationship('CommentModel', back_populates='issue', lazy='dynamic', cascade='all, delete')
  attachments = db.relationship('AttachmentModel', back_populates='issue', lazy='dynamic', cascade='all, delete')

  