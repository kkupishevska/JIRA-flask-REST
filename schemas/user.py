from marshmallow import Schema, fields, validate

# from schemas.project import PlainProjectSchema

class PlainUserSchema(Schema):
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True, validate=validate.Length(max=255))
  password = fields.Str(required=True, load_only=True)
  email = fields.Str(required=True, validate=validate.Email())
  
class UpdateUserSchema(Schema):
  username = fields.Str()
  email = fields.Str(validate=validate.Email())
  password = fields.Str()

class UserSchema(PlainUserSchema):
  projects = fields.List(fields.Nested('PlainProjectSchema', dump_only=True))
  # projectsOwner = fields.List(fields.Nested(PlainProjectSchema(), dump_only=True))

class LoginSchema(Schema):
  email = fields.Str(required=True, validate=validate.Email())
  password = fields.Str(required=True)

