from src.core.database import db
from sqlalchemy import func


class Archivo(db.Model):
    __tablename__ = "archivo"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(120), nullable=False)
    enlace = db.Column(db.String(300), nullable=False)
    fecha_subida = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    tipo = db.Column(
        db.String(30), nullable=False
    )  # como seria para los tipos de los diferentes modulos
