from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(String(64), primary_key=True, index=True)
    order_number = Column(String(64), unique=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float)
    status = Column(String(32))
    user_id = Column(String(64), ForeignKey("users.id"))

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
