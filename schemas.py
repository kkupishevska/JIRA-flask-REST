from marshmallow import Schema, fields, validate

from models import IssueStatus, IssuePriority, IssueType

class PlainProjectSchema(Schema):
  id = fields.Int(dump_only=True)
  projectKey = fields.Str(required=True, validate=validate.Length(max=10))
  projectName = fields.Str(required=True, validate=validate.Length(max=255))
  description = fields.Str()
  createdByUserId = fields.Int()

class PlainUserSchema(Schema):
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True, validate=validate.Length(max=255))
  password = fields.Str(required=True, load_only=True)
  email = fields.Str(required=True, validate=validate.Email())

class PlainIssueSchema(Schema):
  id = fields.Int(dump_only=True)
  summary = fields.Str(validate=validate.Length(max=255), required=True)
  description = fields.Str()
  status = fields.Str(validate=validate.OneOf([str(status.value) for status in IssueStatus]))
  projectId = fields.Int(required=True)

class PlainIssueCommentSchema(Schema):
  id = fields.Int(dump_only=True)
  userId = fields.Int(required=True)
  commentText = fields.Str(required=True, validate=validate.Length(max=1000))

class PlainCommentSchema(PlainIssueCommentSchema):
  issueId = fields.Int(required=True)
  
class UpdateUserSchema(Schema):
  username = fields.Str()
  email = fields.Str(validate=validate.Email())
  password = fields.Str()

class UserSchema(PlainUserSchema):
  projects = fields.List(fields.Nested(PlainProjectSchema(), dump_only=True))
  # projectsOwner = fields.List(fields.Nested(PlainProjectSchema(), dump_only=True))

class LoginSchema(Schema):
  email = fields.Str(required=True, validate=validate.Email())
  password = fields.Str(required=True)

class UpdateProjectSchema(Schema):
  projectKey = fields.Str(validate=validate.Length(max=10))
  projectName = fields.Str(validate=validate.Length(max=255))
  description = fields.Str()
  ownerId = fields.Int()

class ProjectSchema(PlainProjectSchema):
  # createdByUser = fields.Nested(PlainUserSchema, dump_only=True)
  createdByUserId = fields.Int()
  owner = fields.Nested(PlainUserSchema, dump_only=True)
  team_members = fields.List(fields.Nested(PlainUserSchema(), dump_only=True))

  # createdByUser = fields.Nested('UserSchema', exclude=('projects',), dump_only=True)

class IssueSchema(PlainIssueSchema):
  issueKey = fields.Str()
  issueType = fields.Str(validate=validate.OneOf([str(status.value) for status in IssueType]))
  priority = fields.Str(validate=validate.OneOf([str(status.value) for status in IssuePriority]))
  reporterUserId = fields.Int()
  assigneeUserId = fields.Int()
  createdDate = fields.DateTime()
  updatedDate = fields.DateTime()
  reporterUser = fields.Nested(PlainUserSchema, dump_only=True)
  assigneeUser = fields.Nested(PlainUserSchema, dump_only=True)
  comments = fields.List(fields.Nested(PlainCommentSchema(), dump_only=True))
  # attachments = fields.List(fields.Nested(PlainProjectSchema(), dump_only=True))

class IssueSchemaForProject(PlainIssueSchema):
  projectId = fields.Int(required=True)
  issueKey = fields.Str()
  issueType = fields.Str(validate=validate.OneOf([str(status.value) for status in IssueType]))
  priority = fields.Str(validate=validate.OneOf([str(status.value) for status in IssuePriority]))
  reporterUserId = fields.Int()
  assigneeUserId = fields.Int()
  createdDate = fields.DateTime()
  updatedDate = fields.DateTime()
  reporterUser = fields.Nested(PlainUserSchema, dump_only=True)
  assigneeUser = fields.Nested(PlainUserSchema, dump_only=True)

class UpdateIssueSchema(Schema):
  projectId = fields.Int(required=True)
  issueKey = fields.Str()
  summary = fields.Str(validate=validate.Length(max=255))
  description = fields.Str()
  issueType = fields.Str()
  status = fields.Str()
  priority = fields.Str()
  assigneeUserId = fields.Int()
  createdDate = fields.DateTime()
  updatedDate = fields.DateTime()

class ProjectMemberSchema(Schema):
  message = fields.Str()
  project = fields.Nested(PlainProjectSchema)
  user = fields.Nested(PlainIssueSchema)

class CommentSchema(PlainCommentSchema):
  user = fields.Nested(PlainUserSchema, dump_only=True)
  createdDate = fields.DateTime()
  
class UpdateCommentSchema(Schema):
  commentText = fields.Str(validate=validate.Length(max=1000))