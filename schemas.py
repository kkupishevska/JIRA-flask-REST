from marshmallow import Schema, fields, validate

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
  email = fields.Str(required=True)

class UpdateUserSchema(Schema):
  username = fields.Str()
  email = fields.Str()
  password = fields.Str()

class UserSchema(PlainUserSchema):
  projects = fields.List(fields.Nested(PlainProjectSchema(), dump_only=True))

class LoginSchema(Schema):
  email = fields.Str(required=True)
  password = fields.Str(required=True)

class UpdateProjectSchema(Schema):
  projectKey = fields.Str(validate=validate.Length(max=10))
  projectName = fields.Str(validate=validate.Length(max=255))
  description = fields.Str()
  createdByUserId = fields.Int()

class ProjectSchema(PlainProjectSchema):
  createdByUser = fields.Nested(PlainUserSchema, dump_only=True)
  # createdByUser = fields.Nested('UserSchema', exclude=('projects',), dump_only=True)