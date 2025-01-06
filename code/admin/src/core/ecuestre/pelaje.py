from src.core.database import db


class Pelaje(db.Model):
    __tablename__ = "pelaje"
    __table_args__ = {"extend_existing": True}
    id_pelaje = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(30), nullable=False)
