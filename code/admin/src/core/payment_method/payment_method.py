from sqlalchemy import func
from src.core.database import db


class PaymentMethod(db.Model):
    __tablename__ = 'payments_methods'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return (f"<PaymentMethod {self.id} {self.name}")
