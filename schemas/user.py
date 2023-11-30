from marshmallow import Schema, fields, validate
from project import PlainProjectSchema

class PlainUserSchema(Schema):
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True, validate=validate.Length(max=255))
  passwordHash = fields.Str(required=True, load_only=True)
  email = fields.Str(required=True)

class UpdateUserSchema(Schema):
  username = fields.Str()
  email = fields.Str()
  passwordHash = fields.Str()

class UserSchema(PlainUserSchema):
  projects = fields.List(fields.Nested(PlainProjectSchema(), dump_only=True))
