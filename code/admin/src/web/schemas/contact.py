from marshmallow import Schema, fields


class ContactSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    email = fields.Str(required=True)
    cuerpo_mensaje = fields.Str(required=True)
    estado = fields.Str(required=True)
    fecha_creacion = fields.DateTime(dump_only=True)

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
