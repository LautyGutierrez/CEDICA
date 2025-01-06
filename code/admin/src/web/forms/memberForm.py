import datetime
from flask_wtf import FlaskForm
from typing import TypedDict
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    IntegerField,
    EmailField,
    DateField,
    SelectField,
    HiddenField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

data_required = DataRequired("Este campo es requerido")


def setLength(max_length, field):
    return Length(
        max=max_length, message=f"{field} no puede tener más de {max_length} caracteres"
    )


class DeleteMemberForm(FlaskForm):
    csrf_token = HiddenField()


class MemberFormValues(TypedDict):
    nombre: str
    apellido: str
    dni: int
    domicilio: str
    email: str
    localidad: str
    telefono: str
    profesion: str
    puesto_laboral: str
    fecha_inicio: datetime
    nombre_emergencia: str
    telefono_emergencia: str
    obra_social: str
    num_afiliado: int
    condicion: str


class MemberForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[data_required, setLength(30, "Nombre")],
    )

    apellido = StringField(
        "Apellido",
        validators=[data_required, setLength(30, "Apellido")],
    )

    localidad = StringField(
        "Localidad",
        validators=[data_required, setLength(50, "Localidad")],
    )

    domicilio = StringField(
        "Domicilio",
        validators=[data_required, setLength(255, "Domicilio")],
    )

    dni = IntegerField(
        "DNI",
        validators=[
            data_required,
            NumberRange(min=0, message="El DNI debe ser un número válido."),
        ],
    )

    email = EmailField(
        "Email",
        validators=[data_required, setLength(255, "Email")],
    )

    profesion = SelectField(
        "Profesión",
        choices=[
            ("psicologo", "Psicólogo/a"),
            ("psicomotricista", "Psicomotricista"),
            ("medico", "Médico/a"),
            ("kinesiologo", "Kinesólogo/a"),
            ("ocupacional", "Terapista ocupacional"),
            ("psicopedagogo", "Psicopedagogo/a"),
            ("docente", "Docente"),
            ("profesor", "Profesor/a"),
            ("fonoaudiologo", "Fonoaudiólog/a"),
            ("veterinario", "Veterinario/a"),
            ("otro", "Otro"),
        ],
        validators=[data_required],
    )

    puesto_laboral = SelectField(
        "Puesto laboral",
        choices=[
            ("administrativo", "Administrativo/a"),
            ("terapeuta", "Terapeuta"),
            ("conductor", "Conductor"),
            ("pista", "Auxiliar de pista"),
            ("herrero", "Herrero/a"),
            ("veterinario", "Veterinario/a"),
            ("caballos", "Entrenador/a de caballos"),
            ("domador", "Domador/a"),
            ("profesor", "Profesor/a de equitación"),
            ("capacitacion", "Docente de capacitación"),
            ("mantenimiento", "Auxiliar de mantenimiento"),
            ("otro", "Otro"),
        ],
        validators=[data_required],
    )

    fecha_inicio = DateField(
        "Fecha de inicio", format="%Y-%m-%d", validators=[data_required]
    )

    fecha_cese = DateField(
        "Fecha de cese", format="%Y-%m-%d", validators=[Optional()])

    telefono_emergencia = StringField(
        "Teléfono de emergencia",
        validators=[data_required, setLength(20, "Teléfono de emergencia")],
    )

    nombre_emergencia = StringField(
        "Nombre de emergencia",
        validators=[data_required, setLength(20, "Nombre de emergencia")],
    )

    obra_social = StringField(
        "Obra social", validators=[setLength(30, "Obra social"), Optional()]
    )

    num_afiliado = IntegerField(
        "Número de afiliado", validators=[Optional()]
    )

    telefono = StringField(
        "Teléfono",
        validators=[data_required, setLength(20, "Teléfono")],
    )

    condicion = SelectField(
        "Condición",
        choices=[("voluntario", "Voluntario"),
                 ("rentado", "Personal rentado")],
        validators=[data_required],
    )

    def values(self) -> MemberFormValues:
        return {
            "nombre": self.nombre.data,
            "apellido": self.apellido.data,
            "dni": self.dni.data,
            "domicilio": self.domicilio.data,
            "email": self.email.data,
            "localidad": self.localidad.data,
            "telefono": self.telefono.data,
            "profesion": self.profesion.data,
            "puesto_laboral": self.puesto_laboral.data,
            "fecha_inicio": self.fecha_inicio.data,
            "nombre_emergencia": self.nombre_emergencia.data,
            "telefono_emergencia": self.telefono_emergencia.data,
            "obra_social": self.obra_social.data,
            "num_afiliado": self.num_afiliado.data,
            "condicion": self.condicion.data,
        }
