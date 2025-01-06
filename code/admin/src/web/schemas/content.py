from marshmallow import Schema, fields


class ContentSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    summary = fields.Str(required=True)
    content_text = fields.Str(required=True)
    date_creation = fields.DateTime(dump_only=True)
    date_publication = fields.DateTime(dump_only=True)
    date_update = fields.DateTime(dump_only=True)
    email = fields.Str(required=True)
    state = fields.Str(required=True)

content_schema = ContentSchema()
contents_schema = ContentSchema(many=True)
