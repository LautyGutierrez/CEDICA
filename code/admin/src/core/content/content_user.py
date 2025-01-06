from sqlalchemy import func
from src.core.database import db


class ContentUser(db.Model):
    __tablename__ = "content-user"

    id = db.Column(db.Integer, primary_key=True)
    id_content = db.Column(db.Integer, db.ForeignKey("content.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<ContentUser {self.id} {self.id_content} {self.id_user}>"
