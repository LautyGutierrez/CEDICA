from src.core.database import db


class JyATutors(db.Model):
    __tablename__ = 'jya_tutors'

    id = db.Column(db.Integer, primary_key=True)
    jya_id = db.Column(db.Integer, db.ForeignKey('jya.id'), nullable=False)
    tutor_id1 = db.Column(db.Integer, db.ForeignKey(
        'tutors.id'), nullable=False)
    tutor_id2 = db.Column(
        db.Integer, db.ForeignKey('tutors.id'), nullable=True)
