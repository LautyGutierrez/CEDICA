from sqlalchemy import func
from src.core.database import db


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    id_member = db.Column(db.Integer, db.ForeignKey(
        'members.id'), nullable=True)
    id_type_of_payment = db.Column(db.Integer, db.ForeignKey(
        'types_of_payments.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Payment {self.id} {self.id_member} {self.id_type_of_payment} {self.amount} {self.description} {self.date}>'
