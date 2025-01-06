from core.charge.charge import Charge
from core.equipo.miembro import Miembro
from core.jya.jya import JyA
from core.payment_method.payment_method import PaymentMethod
from sqlalchemy import func
from src.core.jya.jya import JyA
from web.forms.charge import ChargeCreateForm
from src.core.database import db
from datetime import datetime, timedelta
import typing as t
import typing_extensions as te


class ChargeService:

    @classmethod
    def create_charge(cls, **kwargs):
        """
        Crea un nuevo cobro.

        Args:
            kwargs: los campos del cobro.

        Returns:  
            Charge: el cobro creado.
        """
        charge = Charge(**kwargs)
        db.session.add(charge)
        db.session.commit()
        return charge

    @classmethod
    def find_charge_by_id(cls, id_charge: int) -> t.Optional[Charge]:
        """
        Retorna información de un cobro determinado por su ID

        Args:
            id_charge: int ID del cobro a buscar

        Returns:   
            Charge: información del cobro encontrado
        """
        return Charge.query.filter_by(id=id_charge).first()

    @classmethod
    def update_charge(cls, charge_id: int, **kwargs: te.Unpack[ChargeCreateForm]) -> t.Optional[Charge]:
        """
        Actualiza la información de un cobro, si existe.

        Args:
            charge_id: int
                ID del cobro a actualizar
            kwargs: los campos a actualizar

        Returns:
            Charge: el cobro actualizado
        """
        charge = db.session.query(Charge).get(charge_id)
        if not charge:
            return None

        for field, value in kwargs.items():
            setattr(charge, field, value)
        db.session.commit()
        return charge

    @classmethod
    def delete_charge(cls, charge_id: int) -> bool:
        """
        Marca un cobro como eliminado.

        Args:
            charge_id: int
                ID del cobro a marcar como eliminado.

        Returns:
            bool: True si se pudo marcar como eliminado, False en caso contrario.
        """
        charge = db.session.query(Charge).get(charge_id)
        if charge:
            setattr(charge, "deleted", True)
            db.session.commit()
            return True
        return False

    @classmethod
    def mark_charge_as_debt(cls, charge_id: int) -> bool:
        """
        Marca un cobro como deuda.

        Args:
            charge_id: int
                ID del cobro a marcar como deuda.

        Returns:
            bool: True si se pudo marcar como deuda, False en caso contrario.
        """
        charge = db.session.query(Charge).get(charge_id)
        if charge:
            setattr(charge, "state", "Deuda")
            db.session.commit()
            return True
        return False

    @classmethod
    def mark_charge_as_paid(cls, charge_id: int) -> bool:
        """
        Marca un cobro como cobrado.

        Args:
            charge_id: int
                ID del cobro a marcar como cobrado.

        Returns:
            bool: True si se pudo marcar como cobrado, False en caso contrario.
        """
        charge = db.session.query(Charge).get(charge_id)
        if charge:
            if charge.state == "Cobrado":
                setattr(charge, "state", "Pendiente")
                db.session.commit()
                return True, "Pendiente"
            setattr(charge, "state", "Cobrado")
            db.session.commit()
            return True, "Cobrado"
        return False

    @classmethod
    def count_charges_for_jya(cls, page: int = 1, per_page: int = 10) -> t.List[t.Tuple[JyA, int]]:
        """
        Cuenta los cobros que se han hecho para cada JyA.

        Args:
            page: int
                página actual
            per_page: int
                cantidad de resultados por página

        Retorna una lista de tuplas [(JyA, count)] donde sólo aparecen los JyA con cobros asociados.
        """
        query = (db.session.query(JyA.id, JyA.name, JyA.lastname, JyA.document_number, JyA.birthdate, JyA.is_debtor, func.count(Charge.id))
                 .join(Charge, Charge.id_jya == JyA.id)
                 .group_by(JyA.id, JyA.name, JyA.lastname)
                 .having(func.count(Charge.id) > 0))

        total = query.count()

        result = query.offset((page - 1) * per_page).limit(per_page).all()

        return result, total

    @classmethod
    def filter_users(
        cls,
        order: t.Optional[str] = 'asc',
        page: int = 1,
        per_page: int = 10,
        tipo_pago: t.Optional[str] = None,
        desde: t.Optional[str] = None,
        hasta: t.Optional[str] = None,
        nombre: t.Optional[str] = None,
        apellido: t.Optional[str] = None,
    ):
        """Filtra cobros, miembros y métodos de pago según los parámetros dados, ordenando por fecha de pago.

        Args:
            order: str
                orden de los resultados (ascendente o descendente)
            page: int
                página actual
            per_page: int
                cantidad de resultados por página
            tipo_pago: str
                tipo de pago
            desde: str
                fecha de inicio
            hasta: str
                fecha de fin
            nombre: str
                nombre del miembro
            apellido: str
                apellido del miembro
        Returns:
            List[Tuple[Charge, Miembro, JyA, PaymentMethod]], int]:
                Un array de tuplas que contiene:
                    - Charge, Miembro, JyA y PaymentMethod.
                Un entero que representa el número total de cobros encontrados.

        """

        query = (db.session.query(Charge, Miembro, JyA, PaymentMethod)
                 .join(Miembro, Charge.id_member == Miembro.id)
                 .join(PaymentMethod, Charge.id_payment_method == PaymentMethod.id)
                 .join(JyA, Charge.id_jya == JyA.id)
                 .filter(Charge.deleted == False)
                 )

        order_direction = Charge.date.desc() if order == 'desc' else Charge.date.asc()

        if tipo_pago:
            query = query.filter(PaymentMethod.name == tipo_pago)
        if desde:
            desde_date = datetime.strptime(desde, '%Y-%m-%d')
            query = query.filter(Charge.date >= desde_date)
        if hasta:
            hasta_date = datetime.strptime(hasta, '%Y-%m-%d')
            query = query.filter(Charge.date <= hasta_date)
        if nombre:
            query = query.filter(Miembro.nombre.ilike(f"%{nombre}%"))
        if apellido:
            query = query.filter(Miembro.apellido.ilike(f"%{apellido}%"))

        query = query.order_by(order_direction)
        total = query.count()
        charge_members_jya_methods = query.offset(
            (page - 1) * per_page).limit(per_page).all()
        return charge_members_jya_methods, total

    @classmethod
    def obtener_ingresos_por_mes(cls):
        """
        Retorna los ingresos por mes de los últimos 12 meses.

        Returns:
            List[Tuple[str, float]]: Lista de tuplas con el mes y el total de ingres
        """
        fecha_actual = datetime.now()
        fecha_inicio = fecha_actual - timedelta(days=365)
        ingresos_por_mes = db.session.query(
            func.date_trunc('month', Charge.date).label('mes'),
            func.sum(Charge.amount).label('cantidad_ingresos')
        ).filter(Charge.date >= fecha_inicio).group_by('mes').order_by('mes').all()

        return ingresos_por_mes