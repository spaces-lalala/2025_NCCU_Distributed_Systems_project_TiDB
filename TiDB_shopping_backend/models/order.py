from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
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

class Category(Base):
    __tablename__ = "categories"

    name = Column(String(100), primary_key=True) 

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(Float)
    image_url = Column(String(255), nullable=True)
    sold = Column(Integer, default=0)
    stock = Column(Integer)
    description = Column(String(1000)) 
    category_name = Column(String(100), ForeignKey("categories.name"))

    category = relationship("Category", back_populates="products")
