from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(64))
    email = Column(String(128), unique=True, index=True)
    password = Column(String(128))

    orders = relationship("Order", back_populates="user")
