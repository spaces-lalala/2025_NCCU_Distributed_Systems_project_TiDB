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
    
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan") #與item設為雙向關聯
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(64), primary_key=True, index=True)
    order_id = Column(String(64), ForeignKey("orders.id"))
    product_id = Column(String(64), ForeignKey("products.id"))
    product_name = Column(String(255))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    
class Product(Base):
    __tablename__ = "products"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0) 