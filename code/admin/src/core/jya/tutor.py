from src.core.database import db


class Tutor(db.Model):
    __tablename__ = "tutors"

    id = db.Column(db.Integer, primary_key=True)
    tutor_relationship = db.Column(db.String(50), nullable=False)
    tutor_name = db.Column(db.String(255), nullable=False)
    tutor_lastname = db.Column(db.String(255), nullable=False)
    tutor_document_number = db.Column(
        db.String(255), unique=True, nullable=False)
    tutor_home_address = db.Column(db.String(50), nullable=False)
    tutor_phone_number = db.Column(db.String(20), nullable=False)
    tutor_email = db.Column(db.String(50), unique=True, nullable=False)
    tutor_educational_level = db.Column(db.String(50), nullable=False)
    tutor_activity = db.Column(db.String(50), nullable=False)
