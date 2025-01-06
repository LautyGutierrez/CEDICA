from src.core.database import db


class MiembroUsuario(db.Model):
    __tablename__ = "miembro-usuario"

    id = db.Column(db.Integer, primary_key=True)
    id_miembro = db.Column(db.Integer, db.ForeignKey("members.id"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<MiembroUsuario {self.id} {self.id_miembro} {self.id_usuario}>"
