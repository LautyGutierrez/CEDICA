from core.auth.roles import Permission, Role, RolePermission
import flask
from sqlalchemy import or_
from web.forms.user import UserUpdateParams
import typing_extensions as te
from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.auth.user import User, PreRegisterUser
from sqlalchemy import exc as sa_exc
import typing as t
from src.core.equipo import MemberService
from src.web.controllers import _helpers as h


class AuthService:
    """Service for handling auth.

    This service is used for handling the first step of the registration
    process and the general permissions of the users.
    """

    # -- Búsqueda de usuarios --
    @classmethod
    def find_user_by_email(cls, email: str) -> t.Optional[User]:
        """Busca un usuario por su correo.

        Args:
            email: str
                correo del usuario

        Returns:
            User: el usuario encontrado
        """
        return User.query.filter_by(email=email).first()
    
    @classmethod
    def find_user_by_email_google(cls, email: str) -> t.Optional[User]:
        """Busca un usuario por su correo.

        Args:
            email: str
                correo del usuario

        Returns:
            User: el usuario encontrado
        """
        return User.query.filter_by(email=email).filter_by(type_register="GOOGLE").first()

    @classmethod
    def find_user_exist(cls, alias: str, email: str) -> t.Optional[User]:
        """Busca si ya existe un usuario con el alias o email dado.

        Args:
            alias: str
                alias del usuario
            email: str
                correo del usuario

        Returns:
            User: el usuario encontrado
        """
        return User.query.filter(or_(User.alias == alias, User.email == email)).first()
    
    @classmethod
    def find_alias(cls, alias: str) -> t.Optional[User]:
        """Busca si ya existe un usuario con el alias o email dado.

        Args:
            alias: str
                alias del usuario
            email: str
                correo del usuario

        Returns:
            User: el usuario encontrado
        """
        return User.query.filter(or_(User.alias == alias)).first()

    @classmethod
    def find_user_by_id(cls, user_id: int) -> t.Optional[User]:
        """Busca un usuario por su ID.

        Args:
            user_id: int
                ID del usuario

        Returns:
            User: el usuario encontrado
        """
        return db.session.query(User).filter(User.id == user_id).first()

    @classmethod
    def filter_users(
        cls,
        email: t.Optional[str],
        active: t.Optional[str],
        rol: t.Optional[str],
        order: t.Optional[str],
        order_by: t.Optional[str],
        page: int = 1,
        per_page: int = 10
    ) -> t.Tuple[t.List[User], int]:
        """Filtra usuarios según los parámetros dados.

        Args:
            email: str
                correo del usuario
            active: str
                estado de la cuenta
            rol: str
                rol del usuario
            order: str
                orden de los resultados (ascendente o descendente)
            order_by: str
                campo por el cual ordenar
            page: int
                página actual
            per_page: int
                cantidad de resultados por página

        Returns:
            Tuple[List[User], int]: lista de usuarios y total de usuarios encontrados

            
        """
        user_session = flask.g.user

        query = db.session.query(User, Role).join(
            Role, User.rol_id == Role.id).filter(User.deleted.is_(False)).filter(User.id != user_session.id)

        filters = {
            "rol": Role.name == rol if rol else None,
            "email": User.email.ilike(f"%{email}%") if email else None,
            "active": User.is_active.is_(True) if active == "True" else (User.is_active.is_(False) if active == "False" else None),
        }

        for condition in filters.values():
            if condition is not None:
                query = query.filter(condition)

        order_columns = {'email': User.email, 'fecha': User.created_at}
        if order_by in order_columns:
            order_direction = order_columns[order_by].desc(
            ) if order == 'desc' else order_columns[order_by].asc()
            query = query.order_by(order_direction)

        total = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()

        return users, total
    

    @classmethod
    def filter_users_deleteds(
        cls,
        page: int = 1,
        per_page: int = 10
    ) -> t.Tuple[t.List[User], int]:
        """Filtra usuarios según los parámetros dados.

        Args:
            email: str
                correo del usuario
            active: str
                estado de la cuenta
            rol: str
                rol del usuario
            order: str
                orden de los resultados (ascendente o descendente)
            order_by: str
                campo por el cual ordenar
            page: int
                página actual
            per_page: int
                cantidad de resultados por página

        Returns:
            Tuple[List[User], int]: lista de usuarios y total de usuarios encontrados

            
        """
       

        query = db.session.query(User, Role).join(
            Role, User.rol_id == Role.id).filter(User.deleted.is_(True))

        total = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()

        return users, total

    # -- Operaciones CRUD con usuarios --
    @classmethod
    def create_user(cls, **kwargs) -> User:
        """Crea un nuevo usuario.

        Args:
            **kwargs: dict
                Campos del usuario

        Returns:
            User: el usuario creado

        """
        hashed_password = bcrypt.generate_password_hash(
            kwargs['password'].encode('utf-8')).decode('utf-8')
        kwargs['password'] = hashed_password
        user = User(**kwargs)
        db.session.add(user)

        from core.equipo.member_user_controller import MemberUser
        miembro = MemberUser.find_member_by_mail(user.email)
        if miembro:
            MemberUser.create_miembro_usuario(
                **{"id_miembro": miembro.id, "id_usuario": user.id})
            h.flash_success("Se asoció al usuario con un miembro")

        db.session.commit()
        return user

    @classmethod
    def update_user(cls, user_id: int, **kwargs: te.Unpack[UserUpdateParams]) -> t.Optional[User]:
        """Actualiza un usuario existente.

        Args:
            user_id: int
                ID del usuario
            **kwargs: dict
                Campos a actualizar

        Returns:
            User: el usuario actualizado
        """
        user = db.session.query(User).get(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.session.commit()
            return user       
        return None

    @classmethod
    def delete_user(cls, user_id: int) -> bool:
        """Marca un usuario como eliminado.

        Args:
            user_id: int
                ID del usuario

        Returns:
            bool: True si se pudo eliminar, False en caso contrario
        """
        user = db.session.query(User).get(user_id)
        if user:
            setattr(user, "deleted", True)
            db.session.commit()
            return True
        return False

    @classmethod
    def toggle_active(cls, user_id: int) -> t.Optional[User]:
        """Activa o desactiva un usuario.

        Args:
            user_id: int
                ID del usuario

        Returns:
            User: el usuario actualizado
        """
        user = db.session.query(User).get(user_id)
        if user:
            user.is_active = not user.is_active
            db.session.commit()
            return user
        return None
    
    @classmethod
    def toggle_deleted(cls, user_id: int) -> t.Optional[User]:
        """Recupera un usuario eliminado.

        Args:
            user_id: int
                ID del usuario

        Returns:
            User: el usuario actualizado

        """
        user = db.session.query(User).get(user_id)
        if user:
            user.deleted = not user.deleted
            db.session.commit()
            return user
        return None

    # -- Gestión de roles y permisos --
    @classmethod
    def change_role_user(cls, user_id: int, role: str) -> bool:
        """Cambia el rol de un usuario.

        Args:
            user_id: int
                ID del usuario
            role: str
                nombre del rol

        Returns:
            bool: True si se pudo cambiar el rol, False en caso
        """
        try:
            role_id = db.session.query(Role.id).filter(
                Role.name == role).scalar()
            if not role_id:
                return False

            db.session.query(User).filter(
                User.id == user_id).update({"role_id": role_id})
            db.session.commit()
        except sa_exc.SQLAlchemyError:
            db.session.rollback()
            return False
        return True

    @classmethod
    def user_is_admin(cls, user_id: int) -> bool:
        """Verifica si un usuario es administrador.

        Args:
            user_id: int
                ID del usuario
        Returns:
            bool: True si el usuario es administrador, False en caso contrario.
        """
        user = cls.find_user_by_id(user_id)
        if not user:
            return False

        role = db.session.query(Role).filter(Role.id == user.rol_id).first()
        return role and role.name in ["ADMINISTRACION", "SYSTEM_ADMIN"]

    @classmethod
    def user_permissions(cls, user_id: int) -> t.Sequence[str]:
        """
        Obtiene los permisos asociados a un usuario.

        Args:
            user_id: int
                ID del usuario
        Returns:
            list: lista de permisos asociados al usuario
        """
        user = cls.find_user_by_id(user_id)
        if not user:
            return []

        permissions = (
            db.session.query(Permission.name)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .join(Role, RolePermission.role_id == Role.id)
            .join(User, User.rol_id == Role.id)
            .filter(User.id == user_id)
            .all()
        )

        return [permission.name for permission in permissions]

    # -- Validación de credenciales --
    @classmethod
    def check_password(cls, password: str, confirm_password: str) -> bool:
        """Valida si las contraseñas coinciden."""
        return password == confirm_password

    @classmethod
    def check_user(cls, email: str, password: str) -> t.Optional[User]:
        """Verifica si el usuario existe y la contraseña es correcta."""
        user = cls.find_user_by_email(email)
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return None

    # -- Información de usuario --
    def get_user(user_id: int) -> t.Optional[User]:
        """Obtiene información detallada de un usuario."""
        result = db.session.query(User, Role).join(
            Role, User.rol_id == Role.id).filter(User.id == user_id).first()

        if result:
            user, role = result
            user_data = {
                "id": user.id,
                "firstname": user.first_name,
                "lastname": user.last_name,
                "email": user.email,
                "alias": user.alias,
                "is_active": user.is_active,
                "role": role.name,
                "deleted": user.deleted
            }
            return user_data
        return None
    
    @classmethod
    def create_user_pre_register(cls, **kwargs) -> PreRegisterUser:
        """Crea un nuevo usuario.

        Args:
            **kwargs: dict
                Campos del usuario

        Returns:
            User: el usuario creado

        """
        pre_user = PreRegisterUser(**kwargs)
        db.session.add(pre_user)
        db.session.commit()
        return pre_user
    
    @classmethod
    def get_pre_user_by_email(cls, email: str) -> PreRegisterUser:
        """Busca un usuario por su correo.

        Args:
            email: str
                correo del usuario

        Returns:
            User: el usuario encontrado
        """
        return PreRegisterUser.query.filter_by(email=email).first()

    @classmethod
    def get_pre_user_by_id(cls, id: int) -> PreRegisterUser:
        """Busca un usuario por su correo.

        Args:
            email: str
                correo del usuario

        Returns:
            User: el usuario encontrado
        """
        return PreRegisterUser.query.filter_by(id=id).first()


    @classmethod
    def filter_pre_users(
        cls,
        page: int = 1,
        per_page: int = 10
    ) -> t.Tuple[t.List[User], int]:
        """
        Filtra usuarios según los parámetros dados.

        Args:
            email: str
                correo del usuario
            active: str
                estado de la cuenta
            rol: str
                rol del usuario
            order: str
                orden de los resultados (ascendente o descendente)
            order_by: str
                campo por el cual ordenar
            page: int
                página actual
            per_page: int
                cantidad de resultados por página

            
        """
       

        query = db.session.query(PreRegisterUser)

        total = query.count()
        preusers = query.offset((page - 1) * per_page).limit(per_page).all()

        return  preusers, total
    
    @classmethod
    def delete_preuser(cls, user_id: int) -> bool:
        """Marca un usuario como eliminado.

        Args:
            user_id: int
                ID del usuario

        Returns:
            bool: True si se pudo eliminar, False en caso contrario
        """
        user = db.session.query(PreRegisterUser).get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    
