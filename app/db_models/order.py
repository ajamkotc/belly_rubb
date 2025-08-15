from sqlalchemy import Column, String, ForeignKey
from app.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"))

    def __repr__(self):
        return f"<Order(id={self.id}, customer_id={self.customer_id})>"
