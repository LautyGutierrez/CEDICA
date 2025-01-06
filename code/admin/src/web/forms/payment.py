from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SelectField, DateField
from wtforms.validators import DataRequired, Length, NumberRange
from core.equipo import MemberService
from core.type_of_payment import TypeOfPaymentService


class PaymentCreateForm(FlaskForm):
    amount = DecimalField(
        "Monto",
        validators=[
            DataRequired("Este campo es requerido"),
            NumberRange(min=0.01, message="El monto debe ser mayor que 0"),
        ],
        places=2
    )
    id_type_of_payment = SelectField(
        "Tipo de Pago",
        validators=[
            DataRequired("Este campo es requerido"),
        ],
        choices=[("", "Seleccionar pago")]
    )
    id_member = SelectField(
        "Miembro",
        choices=[("", "Seleccionar miembro")]
    )
    description = StringField(
        "Descripción",
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

        self.id_type_of_payment.choices.extend([
            (type_of_payment.id, type_of_payment.name)
            for type_of_payment in TypeOfPaymentService.list_type_of_payment()
        ])

    def values(self):
        return {
            "amount": self.amount.data,
            "id_member": self.id_member.data,
            "id_type_of_payment": self.id_type_of_payment.data,
            "description": self.description.data,
            "date": self.date.data
        }
