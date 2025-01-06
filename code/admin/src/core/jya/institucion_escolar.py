from sqlalchemy import func
from src.core.database import db


class InstitucionEscolar(db.Model):
    __tablename__ = "institutions"

    id = db.Column(db.Integer, primary_key=True)
    institution_name = db.Column(db.String(50), nullable=False)
    institution_address = db.Column(db.String(50), nullable=False)
    institution_phone_number = db.Column(db.String(20), nullable=False)
