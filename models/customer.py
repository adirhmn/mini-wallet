from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from db.session import Base
from pydantic import BaseModel
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"

    customer_xid = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    wallets = relationship("Wallet", back_populates="customer")

class CustomerInit(BaseModel):
    customer_xid: str
