from core.payment_method.payment_method import PaymentMethod
import flask_sqlalchemy as fsa
import sqlalchemy as sa
from core import database
from src.core.database import db


class Role(db.Model):
    __tablename__ = "roles"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)


class Permission(db.Model):
    __tablename__ = "permissions"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f"<Permission {self.id} {self.name}>"


class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey(
        'permissions.id'), nullable=False)


def get_roles():
    return db.session.query(Role).all()


def seed_auth(db: fsa.SQLAlchemy):

    PaymentMethod.__table__.create(db.engine, checkfirst=True)

    from src.core.permissions import (
        MODULE_ACTIONS,
        ROLE_MODULE_PERMISSIONS,
        RoleEnum,
    )

    try:
        db.drop_all()
        db.create_all()
        permissions = [
            Permission(name=f"{module.value}_{action.value}")
            for module, actions in MODULE_ACTIONS.items()
            for action in actions
        ]

        # Add all permissions in one go
        db.session.add_all(permissions)
        db.session.commit()  # Commit permissions
        print("Permissions created")

        # Insert roles into the database
        roles = [Role(name=role.value) for role in RoleEnum]
        db.session.add_all(roles)
        db.session.commit()  # Commit roles

        # Insert role permissions
        for role, modules in ROLE_MODULE_PERMISSIONS.items():
            actions = [
                f"{module.value}_{action.value}"
                for module, actions in modules.items()
                for action in actions
            ]

            role_permissions = [
                p
                for p in db.session.execute(
                    sa.select(Permission.id).where(
                        Permission.name.in_(actions))
                ).scalars()
            ]

            role_id = db.session.execute(
                sa.select(Role.id).where(Role.name == role.value)
            ).scalar_one()

            role_permission_data = [
                RolePermission(role_id=role_id, permission_id=permission_id)
                for permission_id in role_permissions
            ]

            if role_permission_data:
                db.session.add_all(role_permission_data)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")


def get_role_by_name(name: str) -> Role:
    return db.session.query(Role).filter_by(name=name).first()
