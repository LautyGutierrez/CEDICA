from core.jya import ServiceJyA as s
from flask_wtf import FlaskForm
from core.equipo import MemberService
from core.payment_method import PaymentMethodService
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms import DateField, DecimalField, SelectField, StringField


class ChargeCreateForm(FlaskForm):
    amount = DecimalField(
        "Monto",
        validators=[
            DataRequired("Este campo es requerido"),
            NumberRange(min=0.01, message="El monto debe ser mayor que 0"),
        ],
        places=2
    )
    id_jya = SelectField(
        "Jinete y Amazona",
        validators=[DataRequired("Este campo es requerido")],
        choices=[("", "Seleccionar JyA")]
    )

    id_member = SelectField(
        "Miembro",
        validators=[
            DataRequired("Este campo es requerido"),
        ],
        choices=[("", "Seleccionar miembro")]
    )
    id_payment_method = SelectField(
        "Metodo de Pago",
        validators=[
            DataRequired("Este campo es requerido"),
        ],
        choices=[("", "Seleccionar pago")]
    )
    observation = StringField(
        "Observación",
        validators=[
            Length(min=0, max=255),
        ],
    )
    date = DateField(
        "Fecha",
        validators=[
            DataRequired("Este campo es requerido"),
            Length(min=0, max=32),
        ],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        members, total = MemberService.all_members()
        self.id_member.choices.extend([
            (member[0].id, f"{member[0].nombre} {member[0].apellido}")
            for member in members
        ])

        self.id_payment_method.choices.extend([
            (method_of_payment.id, method_of_payment.name)
            for method_of_payment in PaymentMethodService.list_payment_methods()
        ])

        self.id_jya.choices.extend([
            (jya.id, f"{jya.name} {jya.lastname}")
            for jya in s.list_jya()
        ])

    def values(self):
        return {
            "amount": self.amount.data,
            "id_member": self.id_member.data,
            "id_payment_method": self.id_payment_method.data,
            "observation": self.observation.data,
            "date": self.date.data
        }
