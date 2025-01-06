from src.core.type_of_payment.type_of_payment import TypeOfPayment
from src.core.database import db

import typing as t


class TypeOfPaymentService:
    @classmethod
    def create_type_of_payment(cls, **kwargs):
        """
        Crea un nuevo tipo de pago.

        Args:
            kwargs: los campos del tipo de pago.

        Returns:
            TypeOfPayment: el tipo de pago creado.
        """
        type_of_payment = TypeOfPayment(**kwargs)
        db.session.add(type_of_payment)
        db.session.commit()
        return type_of_payment

    @classmethod
    def list_type_of_payment(cls):
        """	
        Lista los tipos de pago.

        Returns:
            List[TypeOfPayment]: los tipos de pago.
        """
        return db.session.query(TypeOfPayment).all()
