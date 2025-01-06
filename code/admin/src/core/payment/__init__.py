from core.equipo.miembro import Miembro
from core.type_of_payment.type_of_payment import TypeOfPayment
from src.core.database import db
from src.core.payment.payment import Payment
from datetime import datetime, timedelta
from web.forms.payment import PaymentCreateForm
import typing as t
import typing_extensions as te


class PaymentService:
    @classmethod
    def create_payment(cls, **kwargs):
        """
        Crea un nuevo pago.

        Args:
            kwargs: los campos del pago.

        Returns:
            Payment: el pago creado.
        """
        payment = Payment(**kwargs)
        db.session.add(payment)
        db.session.commit()
        return payment

    @classmethod
    def find_payment_by_id(cls, id_payment: int) -> t.Optional[Payment]:
        """
        Retorna información de un pago determinado por su ID

        Args:
            id_payment: int ID del pago a buscar

        Returns:
            Payment: información del pago encontrado
        """
        return Payment.query.filter_by(id=id_payment).first()

    @classmethod
    def update_payment(cls, payment_id: int, **kwargs: te.Unpack[PaymentCreateForm]) -> t.Optional[Payment]:
        """
        Actualiza la información de un pago, si existe.

        Args:
            payment_id: int
                ID del pago a actualizar

        Returns:
            Payment: el pago actualizado
        """
        payment = db.session.query(Payment).get(payment_id)
        if not payment:
            return None

        for field, value in kwargs.items():
            setattr(payment, field, value)
        db.session.commit()
        return payment

    @classmethod
    def delete_payment(cls, payment_id: int) -> bool:
        """
        Marca un pago como eliminado.

        Args:
            payment_id: int
                ID del pago

        Returns:
            bool: True si se pudo eliminar, False en caso contrario
        """
        payment = db.session.query(Payment).get(payment_id)
        if payment:
            setattr(payment, "deleted", True)
            db.session.commit()
            return True
        return False

    @classmethod
    def filter_users(
        cls,
        order: t.Optional[str] = 'asc',
        page: int = 1,
        per_page: int = 10,
        tipo_pago: t.Optional[str] = None,
        desde: t.Optional[str] = None,
        hasta: t.Optional[str] = None
    ) -> t.Tuple[t.List[t.Tuple[Payment, Miembro, TypeOfPayment]], int]:
        """Filtra pagos, miembros y métodos de pago según los parámetros dados, ordenando por fecha de pago.

        Args:
            order (str): 'asc' o 'desc' para ordenar los resultados de forma ascendente o descendente.
            page (int): número de página.
            per_page (int): cantidad de elementos por página.
            tipo_pago (str): nombre del método de pago.
            desde (str): fecha de inicio del rango de fechas.
            hasta (str): fecha de fin del rango de fechas.

        Returns:
            List[Tuple[Payment, Miembro, TypeOfPayment]], int]: lista de tuplas que contienen:
                - Payment, Miembro y TypeOfPayment.
                Entero que representa el número total de pagos encontrados.

        """

        query = (db.session.query(Payment, Miembro, TypeOfPayment)
                 .outerjoin(Miembro, Payment.id_member == Miembro.id)
                 .join(TypeOfPayment, Payment.id_type_of_payment == TypeOfPayment.id)
                 .filter(Payment.deleted.is_(False)))

        order_direction = Payment.date.desc() if order == 'desc' else Payment.date.asc()

        filters = {
            "tipo_pago": TypeOfPayment.name == tipo_pago if tipo_pago else None,
            "desde": Payment.date >= datetime.strptime(desde, '%Y-%m-%d') if desde else None,
            "hasta": Payment.date < datetime.strptime(hasta, '%Y-%m-%d') + timedelta(days=1) if hasta else None
        }

        for condition in filters.values():
            if condition is not None:
                query = query.filter(condition)

        query = query.order_by(order_direction)

        total = query.count()

        payments_members_types = query.offset(
            (page - 1) * per_page).limit(per_page).all()

        return payments_members_types, total
    
    
    
    @classmethod
    def cobros_por_miembro(cls, fecha_desde, fecha_hasta, miembro_id, page, per_page):
        pagos = db.session.query(
            Miembro.nombre,
            Miembro.apellido,
            Miembro.dni,
            Miembro.email,
            Payment.date,
            Payment.amount,
            Payment.description
        ).join(Payment, Miembro.id == Payment.id_member).filter(
            Payment.id_member == miembro_id,
            Payment.date >= fecha_desde,
            Payment.date <= fecha_hasta
        )
        print(pagos.all())
        total = pagos.count()
        consulta = pagos.offset(
            (page - 1) * per_page).limit(per_page).all()
        return consulta, total
        
    