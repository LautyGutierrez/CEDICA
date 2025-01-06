from src.core.database import db
from sqlalchemy import func


class Contacto(db.Model):
    __tablename__ = 'contacto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    cuerpo_mensaje = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(255), default="pendiente")
    comentario= db.Column(db.String(255), nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return (f"<Contacto {self.id} {self.nombre} {self.apellido} {self.email} {self.cuerpo_mensaje} {self.estado} {self.comentario} {self.fecha_creacion}>")

