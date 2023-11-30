from .. import db

from models.utils import UtilsClass

class AttachmentModel(db.Model, UtilsClass):
  __tablename__ = 'attachment'

  id = db.Column(db.Integer, primary_key=True)
  issueId = db.Column(db.Integer, db.ForeignKey('issue.id'))
  filename = db.Column(db.String(255), nullable=False)
  filePath = db.Column(db.String(255), nullable=False)
  uploadDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
  issue = db.relationship('Issue')
