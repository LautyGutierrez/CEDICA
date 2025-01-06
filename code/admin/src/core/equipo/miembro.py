from sqlalchemy import func
from src.core.database import db


class Miembro(db.Model):
    __tablename__ = "members"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    dni = db.Column(db.Integer(), unique=True, nullable=False)
    domicilio = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    localidad = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    profesion = db.Column(db.String(30), nullable=False)
    puesto_laboral = db.Column(db.String(30), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_cese = db.Column(db.DateTime, nullable=True)
    nombre_emergencia = db.Column(db.String(20), nullable=False)
    telefono_emergencia = db.Column(db.String(20), nullable=False)
    obra_social = db.Column(db.String(20))
    num_afiliado = db.Column(db.Integer, unique=True)
    condicion = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    borrado = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Miembro {self.id} {self.nombre} {self.apellido} {self.dni} {self.email} {self.puesto_laboral} {self.fecha_creacion} {self.activo}>"
