from marshmallow import Schema, fields, validate

# from schemas.project import PlainProjectSchema
# from schemas.issue import PlainIssueSchema

class ProjectMemberSchema(Schema):
  message = fields.Str()
  project = fields.Nested('PlainProjectSchema')
  user = fields.Nested('PlainIssueSchema')
