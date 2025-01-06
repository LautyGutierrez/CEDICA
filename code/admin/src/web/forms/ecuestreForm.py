# src/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Regexp
from src.core.ecuestre.pelaje import Pelaje
from src.core.ecuestre.sexoEcuestre import Sexo
from src.core.ecuestre.raza import Raza
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import HiddenField
from src.core.equipo import Miembro


class DeleteEcuestreForm(FlaskForm):
    csrf_token = HiddenField()


class EcuestreForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(max=30, message="El nombre no puede exceder los 30 caracteres"),
            Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$',
                   message="El nombre solo puede contener letras"),

        ],
    )

    fecha_nacimiento = DateField(
        "Fecha de Nacimiento",
        format='%Y-%m-%d',
        validators=[
            DataRequired("Este campo es requerido"),
        ],
    )

    sexo_id = QuerySelectField(
        "Sexo",
        query_factory=lambda: Sexo.query.all(),
        get_label='descripcion',
        validators=[DataRequired("Este campo es requerido")]
    )

    raza_id = QuerySelectField(
        "Raza",
        query_factory=lambda: Raza.query.all(),
        get_label='descripcion',
        validators=[DataRequired("Este campo es requerido")]
    )

    pelaje_id = QuerySelectField(
        "Pelaje",
        query_factory=lambda: Pelaje.query.all(),
        get_label='descripcion',
        validators=[DataRequired("Este campo es requerido")]
    )

    compra_o_donacion = SelectField(
        "Compra/Donación",
        choices=[
            ('compra', 'Compra'),
            ('donacion', 'Donación')
        ],
        validators=[DataRequired("Este campo es requerido")],
    )
    fecha_ingreso = DateField(
        "Fecha de Ingreso",
        format='%Y-%m-%d',
        validators=[
            DataRequired("Este campo es requerido"),
        ],
    )

    sede = StringField(
        "Sede Asignada",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(max=30, message="La sede no puede exceder los 30 caracteres"),
            Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$',
                   message="El nombre solo puede contener letras"),
        ],
    )
    entrenador = QuerySelectField(
        "Entrenador",
        query_factory=lambda: Miembro.query.filter_by(
            puesto_laboral='caballos').all(),
        get_label='nombre',
        validators=[DataRequired("Este campo es requerido")]
    )
    conductor = QuerySelectField(
        "Conductor",
        query_factory=lambda: Miembro.query.filter_by(
            puesto_laboral='conductor').all(),
        get_label='nombre',
        validators=[DataRequired("Este campo es requerido")]
    )
    tipo_JA = SelectField(
        "Tipo de J&A Asignados",
        choices=[
            ('hipoterapia', 'Hipoterapia'),
            ('monta_terapeutica', 'Monta Terapéutica'),
            ('deporte_ecuestre_adaptado', 'Deporte Ecuestre Adaptado'),
            ('actividades_recreativas', 'Actividades Recreativas'),
            ('equitacion', 'Equitación')
        ],
        validators=[DataRequired("Este campo es requerido")]

    )
