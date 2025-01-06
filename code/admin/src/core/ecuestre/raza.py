from src.core.database import db


class Raza(db.Model):
    __tablename__ = "raza"
    __table_args__ = {"extend_existing": True}
    id_raza = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(30), nullable=False)
