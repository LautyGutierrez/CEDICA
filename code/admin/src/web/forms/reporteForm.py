from flask_wtf import FlaskForm
from wtforms import (
    DateField,
)
from wtforms import validators as v
from wtforms_sqlalchemy.fields import QuerySelectField
from src.core.equipo import Miembro


class ReporteForm(FlaskForm):
    fecha_desde= DateField('Fecha Inicio', format='%Y-%m-%d', validators=[v.DataRequired()])
    fecha_hasta = DateField('Fecha Fin', format='%Y-%m-%d', validators=[v.DataRequired()])
    miembro = QuerySelectField(
        "Miembro",
        query_factory=lambda: Miembro.query.all(),
        get_label='email',
        validators=[v.DataRequired("Este campo es requerido")]
    )