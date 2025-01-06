from core.auth.roles import Role
from sqlalchemy import func
from src.core.database import db


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    alias = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'),
                       nullable=False, default=lambda: get_default_role_id())
    type_register = db.Column(db.String(255), default="MANUAL", nullable=False)
    complete_register = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return (f"<User {self.id} {self.first_name} {self.last_name} {self.email} {self.alias} {self.rol_id} {self.is_active} {self.deleted} {self.created_at} {self.updated_at}>")


def get_default_role_id():
    """Retorna el ID del rol por defecto
    Returns:
        int: ID del rol por defecto

    """
    role = db.session.query(Role).filter_by(name="SIN_ROL").first()
    return role.id if role else None


class PreRegisterUser(db.Model):
    __tablename__ = "pre_register_users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return (f"<PreRegisterUser {self.id} {self.first_name} {self.last_name} {self.email} {self.created_at} {self.updated_at}>")