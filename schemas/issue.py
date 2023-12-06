from marshmallow import Schema, fields, validate

from models import IssueStatus, IssuePriority, IssueType

class EnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value

class PlainIssueSchema(Schema):
  id = fields.Int(dump_only=True)
  summary = fields.Str(validate=validate.Length(max=255), required=True)
  description = fields.Str()
  issueType = EnumField(validate=validate.OneOf([str(status.value) for status in IssueType]))
  priority = EnumField(validate=validate.OneOf([str(status.value) for status in IssuePriority]))
  status = EnumField(validate=validate.OneOf([str(status.value) for status in IssueStatus]))
  projectId = fields.Int(required=True)
  issueKey = fields.Str(required=True, validate=validate.Length(max=10))

class IssueSchema(PlainIssueSchema):
  issueKey = fields.Str()
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
  summary = fields.Str(validate=validate.Length(max=255))
  description = fields.Str()
  issueType = fields.Str(validate=validate.OneOf([str(status.value) for status in IssueType]))
  priority = fields.Str(validate=validate.OneOf([str(status.value) for status in IssuePriority]))
  status = fields.Str(validate=validate.OneOf([str(status.value) for status in IssueStatus]))
  assigneeUserId = fields.Int()

class CreateIssueSchema(PlainIssueSchema):
  reporterUserId = fields.Int()
  assigneeUserId = fields.Int()

class CreateIssueInsideProjectSchema(Schema):
  id = fields.Int(dump_only=True)
  summary = fields.Str(validate=validate.Length(max=255), required=True)
  description = fields.Str()
  issueType = EnumField(validate=validate.OneOf([str(status.value) for status in IssueType]))
  priority = EnumField(validate=validate.OneOf([str(status.value) for status in IssuePriority]))
  status = EnumField(validate=validate.OneOf([str(status.value) for status in IssueStatus]))
  issueKey = fields.Str(required=True, validate=validate.Length(max=10))
  reporterUserId = fields.Int()
  assigneeUserId = fields.Int()