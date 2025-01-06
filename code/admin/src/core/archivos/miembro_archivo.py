from src.core.database import db


class ArchivoMiembro(db.Model):
    __tablename__ = "archivo-miembro"

    id = db.Column(db.Integer, primary_key=True)
    id_archivo = db.Column(db.Integer, db.ForeignKey(
        "archivo.id"), nullable=False)
    id_miembro = db.Column(db.Integer, db.ForeignKey(
        "members.id"), nullable=False)

    def __repr__(self):
        return (
            f"<ArchivoMiembro {self.id} archivo {self.id_archivo} miembro {self.id_miembro}>"
        )
