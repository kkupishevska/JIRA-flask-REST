from marshmallow import Schema, fields, validate

# from schemas.user import PlainUserSchema

class PlainProjectSchema(Schema):
  id = fields.Int(dump_only=True)
  projectKey = fields.Str(required=True, validate=validate.Length(max=10))
  projectName = fields.Str(required=True, validate=validate.Length(max=255))
  description = fields.Str()
  createdByUserId = fields.Int()

class UpdateProjectSchema(Schema):
  projectKey = fields.Str(validate=validate.Length(max=10))
  projectName = fields.Str(validate=validate.Length(max=255))
  description = fields.Str()
  ownerId = fields.Int()

class ProjectSchema(PlainProjectSchema):
  # createdByUser = fields.Nested(PlainUserSchema, dump_only=True)
  createdByUserId = fields.Int()
  owner = fields.Nested('PlainUserSchema', dump_only=True)
  team_members = fields.List(fields.Nested('PlainUserSchema', dump_only=True))

  # createdByUser = fields.Nested('UserSchema', exclude=('projects',), dump_only=True)