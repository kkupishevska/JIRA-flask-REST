from db import db

from models.utils import UtilsClass

class CommentModel(db.Model, UtilsClass):
  __tablename__ = 'comment'

  id = db.Column(db.Integer, primary_key=True)
  issueId = db.Column(db.Integer, db.ForeignKey('issue.id'))
  userId = db.Column(db.Integer, db.ForeignKey('user.id'))
  commentText = db.Column(db.Text, nullable=False)
  createdDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
  user = db.relationship('UserModel', foreign_keys=[userId])
  issue = db.relationship('IssueModel', foreign_keys=[issueId], back_populates='comments')