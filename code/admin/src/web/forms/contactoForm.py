from flask_wtf import FlaskForm
from wtforms import StringField, SelectField


class ContactoEditForm(FlaskForm):
    comentario = StringField("Comentario")
    estado = SelectField(
        "Estado",
        choices=[
            ("pendiente", "Pendiente"),
            ("en_proceso", "En proceso"),
            ("rechazado", "Rechazado"),
            ("cancelado", "Cancelado"),
            ("completado", "Completado"),
        ],
    )
