from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField
from wtforms.validators import DataRequired, Length

data_required = DataRequired("Este campo es requerido")


def setLength(max_length, field):
    return Length(
        max=max_length, message=f"{field} no puede tener más de {max_length} caracteres"
    )


class ContentForm(FlaskForm):

    titulo = StringField("Título", validators=[data_required, setLength(100, "Título")])

    resumen = StringField(
        "Resumen", validators=[data_required, setLength(100, "Resumen")]
    )

    texto = TextAreaField("Texto", validators=[data_required])

    def values(self):
        return {
            "titulo": self.titulo.data,
            "resumen": self.resumen.data,
            "texto": self.texto.data,
        }
