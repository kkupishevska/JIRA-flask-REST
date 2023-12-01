from db import db

class ProjectsMembersModel(db.Model):
  __tablename__ = 'project_members'

  id = db.Column(db.Integer, primary_key=True)
  userId = db.Column(db.Integer, db.ForeignKey('user.id'))
  projectId = db.Column(db.Integer, db.ForeignKey('project.id'))
  user = db.relationship('UserModel', foreign_keys=[userId])
