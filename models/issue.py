from db import db

from models.utils import UtilsClass
import enum

class IssueStatus(enum.Enum):
  OPEN="open"                 #The issue is open and ready for the assignee to start work on it.
  INPROGRESS="in_progress"    #This issue is being actively worked on at the moment by the assignee.
  DONE="done"                 #Work has finished on the issue.
  TODO="to_do"                #The issue has been reported and is waiting for the team to action it.
  INREVIEW="in_review"        #The assignee has carried out the work needed on the issue, and it needs peer review before being considered done.
  UNDERREVIEW="under_review"  #A reviewer is currently assessing the work completed on the issue before considering it done.
  APPROVED="approved"         #A reviewer has approved the work completed on the issue and the issue is considered done.
  CANCELLED="ancelled"        #Work has stopped on the issue and the issue is considered done.
  REJECTED="rejected"         #A reviewer has rejected the work completed on the issue and the issue is considered done.

class IssuePriority(enum.Enum):
  BLOCKER="blocker"
  CRITICAL="critical"
  MAJOR="major"
  HIGHEST = "highest" #This problem will block progress.
  HIGH = "high" #Serious problem that could block progress.
  MEDIUM = "medium" #Has the potential to affect progress.
  LOW="low" #Minor problem or easily worked around.
  LOWEST="lowest" #Trivial problem with little or no impact on progress.
  REGULAR="regular"
  MINOR="minor"
  TRIVIAL="trivial"

class IssueType(enum.Enum):
  EPIC='epic'
  BUG='bug'
  IMPROVEMENT='improvement'
  FEATURE='feature'
  STORY='story'
  TASK='task'
  # SUBTASK='subtask'

class IssueModel(db.Model, UtilsClass):
  __tablename__ = 'issue'

  id = db.Column(db.Integer, primary_key=True)
  projectId = db.Column(db.Integer, db.ForeignKey('project.id'))
  issueKey = db.Column(db.String(15), nullable=False)
  summary = db.Column(db.String(255), nullable=False)
  description = db.Column(db.Text)
  issueType = db.Column(db.Enum(IssueType, values_callable=lambda x: [str(item.value) for item in IssueType]), default=IssueType.TASK.value)
  # issueType = db.Column(db.Enum(IssueType), default=IssueType.TASK.value)
  status = db.Column(db.Enum(IssueStatus, values_callable=lambda x: [str(item.value) for item in IssueStatus]), default=IssueStatus.OPEN.value)
  # status = db.Column(db.Enum(IssueStatus), default=IssueStatus.OPEN.value)
  priority = db.Column(db.Enum(IssuePriority, values_callable=lambda x: [str(item.value) for item in IssuePriority]), default=IssuePriority.TRIVIAL.value)
  # priority = db.Column(db.Enum(IssuePriority), default=IssuePriority.TRIVIAL.value)
  reporterUserId = db.Column(db.Integer, db.ForeignKey('user.id'))
  assigneeUserId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
  createdDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
  updatedDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
  reporterUser = db.relationship('UserModel', foreign_keys=[reporterUserId], back_populates='reportedIssues')
  assigneeUser = db.relationship('UserModel', foreign_keys=[assigneeUserId], back_populates='assignedIssues')
  # assigneeUser = db.relationship('UserModel', back_populates='assignedIssues')

  project = db.relationship('ProjectModel', foreign_keys=[projectId], back_populates='issues')
  comments = db.relationship('CommentModel', back_populates='issue', lazy='dynamic', cascade='all, delete')
  attachments = db.relationship('AttachmentModel', back_populates='issue', lazy='dynamic', cascade='all, delete')

  