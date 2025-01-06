from sqlalchemy import asc, desc, func, String
from src.core.database import db
from src.core.equipo.miembro import Miembro
from src.core.equipo.miembro_usuario import MiembroUsuario
from src.core.archivos.archivo import Archivo
from src.core.archivos.miembro_archivo import ArchivoMiembro
import typing as t
from src.core.auth import User


class MemberService:

    @classmethod
    def all_members(
        cls,
        order_field: str = "nombre",
        order_type: str = "asc",
        job: t.Optional[str] = None,
        filter_field: t.Optional[str] = None,
        filter_input: t.Optional[str] = None,
        page: int = 1,
        per_page: int = 10,
    ) -> t.Tuple[
        t.List[t.Tuple[Miembro, t.Optional[MiembroUsuario], t.Optional[User]]], int
    ]:
        """
        Traer todos los miembros de la base de datos que no estén borrados;
        filtrándolos por los campos establecidos y ordenándolos
        haciendo un join con la tabla MiembroUsuario y Usuario.
        Args:
            order_field: str
                Campo para ordenar, por defecto nombre
            order_type: str
                Tipo de orden (ascendente o descendente), por defecto asc
            job: str
                Trabajo para filtrar, por defecto None
            filter_field: str
                Campo para realizar el filtro de búsqueda, por defecto None
            filter_input: str
                Query ingresado para filtrar en el campo filter_field, por defecto None
            page: int
                Página actual para la paginación, por defecto 1
            per_page: int
                Cantidad de resultados por página para la paginación, por defecto 10
        Returns:
            List[Tuple[Miembro, Optional[MiembroUsuario], Optional[User]]], int]:
                Un array de tuplas que contiene:
                    - Miembro, su registro en la tabla MiembroUsuario (si existe, sino None) y su usuario (si existe, sino None).
                Un entero que representa el número total de miembros encontrados.
        """

        query = (
            db.session.query(Miembro, MiembroUsuario, User)
            .select_from(Miembro)
            .outerjoin(MiembroUsuario, Miembro.id == MiembroUsuario.id_miembro)
            .outerjoin(User, MiembroUsuario.id_usuario == User.id)
            .filter(Miembro.borrado == False)
        )

        order = asc(order_field) if order_type == "asc" else desc(order_field)

        if job:
            query = query.filter(Miembro.puesto_laboral == job)

        if filter_field and filter_input:
            if filter_field == "dni":
                query = query.filter(
                    func.cast(Miembro.dni, String).ilike(f"%{filter_input}%")
                )
            else:
                query = query.filter(
                    getattr(Miembro, filter_field).ilike(f"%{filter_input}%")
                )
        query = query.order_by(order)
        total = query.count()
        members = query.offset((page - 1) * per_page).limit(per_page).all()
        return members, total

    @classmethod
    def find_member_by_mail(cls, email: str) -> t.Optional[Miembro]:
        """
        Retorna información de un miembro determinado por su email.

        Args:
            email: str 
                Email del miembro a buscar.

        Returns:
            Miembro: 
                Miembro encontrado, None si no se encuentra.
        """
        return Miembro.query.filter_by(email=email, borrado=False).first()

    @classmethod
    def find_member_by_dni(cls, dni: str) -> t.Optional[Miembro]:
        """
        Retorna información de un miembro determinado por su DNI.

        Args:
            dni: str 
                DNI del miembro a buscar.

        Returns:
            Miembro: 
                Miembro encontrado, None si no se encuentra.
        """
        return Miembro.query.filter_by(dni=dni).first()

    @classmethod
    def find_member_by_num(cls, num: int) -> t.Optional[Miembro]:
        """
        Retorna información de un miembro determinado por su número de afiliado.

        Args:
            num: int 
                Número de afiliado del miembro a buscar.

        Returns:
            Miembro: 
                Miembro encontrado, None si no se encuentra.
        """
        return Miembro.query.filter_by(num_afiliado=num).first()

    @classmethod
    def get_member(cls, id: int) -> t.Optional[Miembro]:
        """
        Retorna información de un miembro determinado por su ID.
        Args:
            id: ID del miembro a buscar.

        Returns:
            Miembro:
                Miembro encontrado, None si no se encuentra.

        """
        return Miembro.query.filter_by(id=id).first()

    @classmethod
    def update_member(cls, member_id: int, form) -> t.Optional[Miembro]:
        """
        Actualiza la información de un miembro, si existe.

        Args:
            member_id: int
                ID del miembro a actualizar.
            form:
                Formulario con los campos a actualizar.
        
        Returns:
            Miembro:
                Miembro actualizado, None si no se encuentra o si se produce un error.
        
        Raises:
            Exception:
                Si hay un error al actualizar la información del miembro en la base de datos.
        """
        member = db.session.query(Miembro).get(member_id)
        if not member:
            return None

        try:
            columns = {c.name: c.nullable for c in Miembro.__table__.columns}

            for field, value in form.items():
                if hasattr(member, field):
                    if columns.get(field, False) and value == "":
                        setattr(member, field, None)
                    else:
                        setattr(member, field, value)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return None

        return member

    @classmethod
    def delete_member(cls, member_id: int) -> bool:
        """
        Elimina lógicamente a un miembro, si existe.

        Args:
            member_id: int
                ID del miembro a eliminar

        Returns:
            bool: 
                True si se pudo marcar como borrado;
                False si el miembro no existe o no se pudo completar la operación.

        Raises:
            Exception: 
                Si hay un error sin manejar al editar la BD.
        """
        member = db.session.query(Miembro).get(member_id)
        if not member:
            return False

        try:
            setattr(member, "borrado", True)
            db.session.commit()
        except:
            db.session.rollback()
            return False

        return True

    @classmethod
    def change_status(cls, member_id: int) -> bool:
        """
        Cambia el estado de un miembro, si existe.

        Args:
            member_id: int: 
                ID del miembro al cual se le cambiará su estado.

        Returns:
            bool: 
                True si se pudo cambiar el estado;
                False si el miembro no existe o no se pudo completar la operación.

        Raises:
            Exception: 
                Si hay un error sin manejar al editar la BD.
        """
        member = db.session.query(Miembro).get(member_id)

        if not member:
            return False

        try:
            member.activo = not member.activo
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False
        return True
