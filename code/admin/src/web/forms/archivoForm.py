from src.web.forms.validators import file_size_limit
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SelectField
from flask_wtf.file import FileAllowed
from wtforms.validators import Regexp, DataRequired, Length


class Archivo(FlaskForm):
    archivo = FileField(
        "Archivo",
        validators=[
            FileAllowed(
                ["pdf", "doc", "xls", "jpeg"],
                "En este campo solo se permiten documentos con la extension pdf, doc, xls, jpeg",
            ),
            DataRequired("Este campo es requerido"),
            file_size_limit(5),
        ],
    )
    titulo = StringField(
        "Título del archivo",
        validators=[DataRequired("Este campo es requerido")],
    )


class ArchivoEcuestreForm(Archivo):
    tipo_archivo = SelectField(
        "Tipo del archivo",
        choices=[
            ("ficha", "Ficha"),
            ("planificacion", "Planificación"),
            ("informe", "Informe"),
            ("imagen", "Imágenes"),
            ("registros_veterinarios", "Registros veterinarios"),
        ],
        validators=[DataRequired("Este campo es requerido")],
    )


class ArchivoJyAForm(Archivo):
    tipo = SelectField(
        "Tipo del archivo",
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

class ArchivoMiembroForm(Archivo):
    tipo_archivo = SelectField(
        "Tipo del archivo",
        choices=[
            ("personal", "Documentación personal"),
            ("educativa", "Documentación educativa"),
            ("laboral", "Documentación laboral"),
            ("extra", "Documentación extra"),
        ],
        validators=[DataRequired("Este campo es requerido")],
    )
