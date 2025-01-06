from src.core.auth import AuthService
from src.core.database import db
from src.core.equipo.miembro import Miembro
from src.core.equipo.miembro_usuario import MiembroUsuario
from src.web.controllers import _helpers as h
import typing as t


class MemberUser:
    """
    Controlador para evitar import circular
    """

    @classmethod
    def create_miembro_usuario(cls, **kwargs):
        miembro_usuario = MiembroUsuario(**kwargs)
        db.session.add(miembro_usuario)
        db.session.commit()
        return miembro_usuario

    @classmethod
    def create_miembro(cls, **kwargs):
        miembro = Miembro(**kwargs)
        # Asociar usuario con miembro
        db.session.add(miembro)
        usuario = AuthService.find_user_by_email(miembro.email)
        if usuario:
            member_usuario_data = {
                "id_miembro": miembro.id, "id_usuario": usuario.id}
            cls.create_miembro_usuario(**member_usuario_data)
        db.session.commit()
        return miembro, usuario

    @classmethod
    def find_member_by_mail(cls, email: str) -> t.Optional[Miembro]:
        return Miembro.query.filter_by(email=email, borrado=False).first()
