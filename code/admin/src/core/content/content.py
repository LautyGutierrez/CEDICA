from sqlalchemy import func
from src.core.database import db


class Content(db.Model):
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(100), nullable=False)
    content_text = db.Column(db.Text, nullable=False)
    date_publication = db.Column(db.DateTime)
    date_creation = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    date_update = db.Column(db.DateTime)
    state = db.Column(db.String(9), nullable=False, default="borrador")
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Content {self.id} {self.title} {self.summary} {self.date_publication} {self.content_text} {self.date_creation} {self.date_update} {self.state}>"
