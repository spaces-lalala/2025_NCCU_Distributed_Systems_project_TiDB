from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(64))
    email = Column(String(128), unique=True, index=True)
    password = Column(String(128))

    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"

    id = Column(String(64), primary_key=True, index=True)
    order_number = Column(String(64), unique=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float)
    status = Column(String(32))
    user_id = Column(String(64), ForeignKey("users.id"))

    user = relationship("User", back_populates="orders")
