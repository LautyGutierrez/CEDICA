from src.core.database import db


class Ecuestre(db.Model):
    __tablename__ = "ecuestre"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    compra_o_donacion = db.Column(db.String(10), nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    sede = db.Column(db.String(30), nullable=False)
    sexo_id = db.Column(db.Integer, db.ForeignKey(
        "sexo.id_sexo"), nullable=False)
    raza_id = db.Column(db.Integer, db.ForeignKey(
        "raza.id_raza"), nullable=False)
    pelaje_id = db.Column(db.Integer, db.ForeignKey(
        "pelaje.id_pelaje"), nullable=False)
    tipo_JA = db.Column(db.String(30), nullable=False)
    borrado = db.Column(db.Boolean, default=False)
    entrenador = db.Column(db.Integer, db.ForeignKey(
        "members.id"), nullable=False)
    conductor = db.Column(db.Integer, db.ForeignKey(
        "members.id"), nullable=False)
