from sqlalchemy import func
from src.core.database import db


class Charge(db.Model):
    __tablename__ = 'charges'

    id = db.Column(db.Integer, primary_key=True)
    id_jya = db.Column(db.Integer, db.ForeignKey('jya.id'), nullable=False)
    id_member = db.Column(db.Integer, db.ForeignKey(
        'members.id'), nullable=False)
    id_payment_method = db.Column(db.Integer, db.ForeignKey(
        'payments_methods.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    observation = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    state = db.Column(db.String(255), nullable=False, default="Pendiente")
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return (f"<Cobro {self.id} {self.id_jya} {self.id_member} {self.id_payment_method} {self.amount} {self.observation} {self.date}>")
