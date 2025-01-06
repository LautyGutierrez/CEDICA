from src.core.database import db
import typing as t
from core.auth.roles import Role


class RoleService:
    
    @classmethod
    def list_roles(cls) -> t.List[Role]:
        """Lista los roles disponibles."""
        return db.session.query(Role).all()
