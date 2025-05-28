# models/item.py
from sqlalchemy import Column, String, Integer, Float
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    quantity = Column(Integer)
