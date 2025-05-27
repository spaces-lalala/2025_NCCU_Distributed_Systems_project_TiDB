from sqlalchemy import Column, Integer, String, Float, Text
from database import Base  # 你應該有定義 Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    reserved_stock = Column(Integer, default=0) 