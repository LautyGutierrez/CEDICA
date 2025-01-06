from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from src.web.forms.validators import title_required_if_file_filled
from wtforms.validators import Regexp, DataRequired, Length, URL


class EnlaceForm(FlaskForm):

    enlace = StringField(
        "Enlace",
        validators=[
            DataRequired("Este campo es obligatorio."),
            URL(message="Ingrese un enlace válido."),
        ],
    )

    titulo = StringField("Titulo", validators=[DataRequired("Este campo es requerido")])


class EnlaceJyAForm(EnlaceForm):
    tipo = SelectField(
        "Tipo de archivo",
        choices=[
            ("entrevista", "Entrevista"),
            ("evaluacion", "Evaluación"),
            ("planificaciones", "Planificaciones"),
            ("evolucion", "Evolución"),
            ("cronicas", "Crónicas"),
            ("documental", "Documental"),
        ],
        validators=[DataRequired("Este campo es requerido"), Length(max=15)],
    )
