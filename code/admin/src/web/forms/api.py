import typing as t
import wtforms
from flask_wtf import FlaskForm
from wtforms import validators as v


class RequestContactFormValues(t.TypedDict):
    nombre: str
    apellido: str
    email: str
    cuerpo_mensaje: str
    recaptcha_token: str

class RequestContactForm(FlaskForm):

    nombre = wtforms.StringField("Nombre", validators=[v.DataRequired()])
    apellido = wtforms.StringField("Apellido", validators=[v.DataRequired()])
    email = wtforms.StringField("Email", validators=[v.DataRequired()])
    cuerpo_mensaje = wtforms.StringField("Cuerpo del mensaje", validators=[v.DataRequired()])
    recaptcha_token = wtforms.StringField("Token de recaptcha", validators=[v.DataRequired()])


    def values(self) -> RequestContactFormValues:
        return {
            "nombre": self.nombre.data,
            "apellido": self.apellido.data,
            "email": self.email.data,
            "cuerpo_mensaje": self.cuerpo_mensaje.data,
            "recaptcha_token": self.recaptcha_token.data,
        }
    





