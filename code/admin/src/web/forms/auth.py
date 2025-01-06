from typing import TypedDict

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    HiddenField,
    PasswordField,
    SelectField,
    StringField,
    StringField,
    PasswordField,
)
from wtforms import validators as v
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginFormValues(TypedDict):
    email: str
    password: str


class UserLogin(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=64),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )

    def values(self) -> LoginFormValues:
        return {  # type: ignore
            "email": self.email.data,
            "password": self.password.data,
        }



class UserPreRegister(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=64),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
        ],
    )

    def values(self):
        return {  # type: ignore
            "firstname": self.firstname.data,
            "lastname": self.lastname.data,
            "email": self.email.data,
        }


class UserRegisterFormValues(TypedDict):
    alias: str
    password: str
    password_confirmation: str


class UserRegisterGoogleFormValues(TypedDict):
    email: str
    alias: str
    password: str
    password_confirmation: str


class UserRegisterGoogle(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=64),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
        ],
    )

    alias = StringField("Alias",
                        validators=[DataRequired("Este campo es requerido")])

    password = PasswordField(
        "Contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
            v.EqualTo(
                "password_confirmation", message="Las contraseñas no coinciden"
            ),
        ],
    )
    password_confirmation = PasswordField(
        "Confirmar contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=6, max=32),
        ],
    )

    def values(self):
        return {
            "username": self.alias.data,
            "email": self.email.data,
            "password": self.password.data,
        }


class UserRegister(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=64),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
        ],
    )

    alias = StringField("Alias",
                        validators=[DataRequired("Este campo es requerido")])

    password = PasswordField(
        "Contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=6, max=32),
            v.EqualTo("password_confirmation",
                      message="Las contraseñas no coinciden"),
        ],
    )
    password_confirmation = PasswordField(
        "Confirmar contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=6, max=32),
        ],
    )

    def values(self):
        return {
            "first_name": self.firstname.data,
            "last_name": self.lastname.data,
            "alias": self.alias.data,
            "email": self.email.data,
            "password": self.password.data,

        }


class UserUpdateParams(TypedDict):
    firstname: str
    lastname: str
    email: str
    alias: str


class ProfileUpdateForm(FlaskForm):

    firstname = StringField(
        "Nombre",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )

    email = EmailField(
        "Email",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=64),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
        ],
    )

    alias = HiddenField(
        "Alias",
        validators=[DataRequired("Este campo es requerido")]
    )

    def values(self) -> UserUpdateParams:
        """Return form values as a dictionary"""

        return {
            "first_name": self.firstname.data,
            "last_name": self.lastname.data,
            "email": self.email.data,
            "alias": self.alias.data,

        }


class SeedForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])




class UserUpdatePreRegisterToUserForm(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=64),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
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
            "rol_id": self.role.data,
        }
    

class CompleteRegister(FlaskForm):
    alias = StringField("Alias",
                        validators=[DataRequired("Este campo es requerido")])

    password = PasswordField(
        "Contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=6, max=32),
            v.EqualTo("password_confirmation",
                        message="Las contraseñas no coinciden"),
        ],
    )
    password_confirmation = PasswordField(
        "Confirmar contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=6, max=32),
        ],
    )

    def values(self):
        return {
            "alias": self.alias.data,
            "password": self.password.data,
        }