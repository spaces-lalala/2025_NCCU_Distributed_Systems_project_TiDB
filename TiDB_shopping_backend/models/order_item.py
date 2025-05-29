from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(64), primary_key=True, index=True)
    order_id = Column(String(64), ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product_name = Column(String(255))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
