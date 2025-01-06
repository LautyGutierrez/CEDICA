from src.core.database import db


class ArchivoEcuestre(db.Model):
    __tablename__ = "archivo-ecuestre"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    archivo_id = db.Column(db.Integer, db.ForeignKey(
        "archivo.id"), nullable=False)
    ecuestre_id = db.Column(db.Integer, db.ForeignKey(
        "ecuestre.id"), nullable=False)
