from marshmallow import Schema, fields, validate

from models import IssueStatus, IssuePriority, IssueType
# from schemas.user import PlainUserSchema
# from schemas.comment import PlainCommentSchema

class PlainIssueSchema(Schema):
  id = fields.Int(dump_only=True)
  summary = fields.Str(validate=validate.Length(max=255), required=True)
  description = fields.Str()
  status = fields.Str(validate=validate.OneOf([str(status.value) for status in IssueStatus]))
  projectId = fields.Int(required=True)

class IssueSchema(PlainIssueSchema):
  issueKey = fields.Str()
  issueType = fields.Str(validate=validate.OneOf([str(status.value) for status in IssueType]))
  priority = fields.Str(validate=validate.OneOf([str(status.value) for status in IssuePriority]))
  reporterUserId = fields.Int()
  assigneeUserId = fields.Int()
  createdDate = fields.DateTime()
  updatedDate = fields.DateTime()
  reporterUser = fields.Nested('PlainUserSchema', dump_only=True)
  assigneeUser = fields.Nested('PlainUserSchema', dump_only=True)
  comments = fields.List(fields.Nested('PlainCommentSchema', dump_only=True))
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
  reporterUser = fields.Nested('PlainUserSchema', dump_only=True)
  assigneeUser = fields.Nested('PlainUserSchema', dump_only=True)

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
