from marshmallow import Schema, fields, validate

# from schemas.user import PlainUserSchema

class PlainIssueCommentSchema(Schema):
  id = fields.Int(dump_only=True)
  userId = fields.Int(required=True)
  commentText = fields.Str(required=True, validate=validate.Length(max=1000))

class PlainCommentSchema(PlainIssueCommentSchema):
  issueId = fields.Int(required=True)

class CommentSchema(PlainCommentSchema):
  user = fields.Nested('PlainUserSchema', dump_only=True)
  createdDate = fields.DateTime()
  
class UpdateCommentSchema(Schema):
  commentText = fields.Str(validate=validate.Length(max=1000))