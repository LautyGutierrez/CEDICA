from src.core.database import db


class ArchivoJyA(db.Model):
    __tablename__ = "archivo-jya"

    id = db.Column(db.Integer, primary_key=True)
    archivo_id = db.Column(db.Integer, db.ForeignKey(
        'archivo.id'), nullable=False)
    jya_id = db.Column(db.Integer, db.ForeignKey('jya.id'), nullable=False)
