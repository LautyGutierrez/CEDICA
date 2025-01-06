from core.payment_method.payment_method import PaymentMethod
from src.core.database import db
import typing as t


class PaymentMethodService:

    @classmethod
    def create_payment_method(cls, **kwargs):
        """
        Crea un nuevo método de pago.

        Args:
            kwargs: los campos del método de pago.

        Returns:
            PaymentMethod: el método de pago creado.
        """

        payment = PaymentMethod(**kwargs)
        db.session.add(payment)
        db.session.commit()
        return payment

    @classmethod
    def list_payment_methods(cls):
        """
        Lista los métodos de pago.

        Returns:
            List[PaymentMethod]: los métodos de pago.
        """

        return db.session.query(PaymentMethod).all()
