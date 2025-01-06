from src.core.database import db


class Sexo(db.Model):
    __tablename__ = "sexo"
    __table_args__ = {"extend_existing": True}
    id_sexo = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(15), nullable=False)
