from sqlalchemy import func
from src.core.database import db


class TypeOfPayment(db.Model):
    __tablename__ = 'types_of_payments'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return (f"<TypeOfPayment {self.id} {self.name}")
