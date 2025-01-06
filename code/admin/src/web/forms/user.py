

import typing as t
from core.roles import RoleService
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField, StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from src.core.enums import DocumentTypes, GenderOptions
from wtforms import validators as v


class UserParams(t.TypedDict):
    firstname: str
    lastname: str
    password: str
    email: str
    alias: str


class UserUpdateParams(t.TypedDict):
    firstname: str
    lastname: str
    role: str


class ProfileUpdateForm(FlaskForm):

    firstname = StringField(
        "Nombre",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(min=0, max=32),
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(min=0, max=32),
        ],
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(min=0, max=64),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
        ],
    )

    alias = StringField("Alias",
                        validators=[DataRequired("Este campo es requerido")])

    role = SelectField(
        "Rol",
        choices=[],
        validators=[DataRequired("Este campo es requerido")],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        roles = RoleService.list_roles()  
        
       
        self.role.choices = [("", "Seleccionar Rol")]  
        self.role.choices.extend([
            (role.id, role.name) for role in roles
        ])

    def values(self) -> UserUpdateParams:
        """Return form values as a dictionary"""

        return {
            "first_name": self.firstname.data,
            "last_name": self.lastname.data,
            "email": self.email.data,
            "alias": self.alias.data,
            "rol_id": self.role.data,

        }


class UserCreateForm(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(min=0, max=32),
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(min=0, max=32),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(min=0, max=64),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
        ],
    )

    alias = StringField("Alias",
                        validators=[DataRequired("Este campo es requerido")])

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(min=6, max=32),
            EqualTo("password_confirmation",
                    message="Las contraseñas no coinciden"),
        ],
    )
    password_confirmation = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(min=6, max=32),
        ],
    )

    role = SelectField(
        "Rol",
        choices=[],
        validators=[DataRequired("Este campo es requerido")],
    )

    def values(self):
        return {
            "first_name": self.firstname.data,
            "last_name": self.lastname.data,
            "alias": self.alias.data,
            "email": self.email.data,
            "password": self.password.data,
            "rol_id": self.role.data,
        }
