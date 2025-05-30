# models/item.py
from sqlalchemy import Column, String, Integer, Float
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(1000), nullable=True)
    price = Column(Float)
    quantity = Column(Integer)
