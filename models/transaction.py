from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from db.session import Base
from datetime import datetime
from pydantic import BaseModel
import uuid

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True, unique=True)
    wallet_id = Column(String, ForeignKey('wallets.id'))
    transaction_type = Column(String)  # 'deposit' or 'withdrawal'
    amount = Column(Integer)
    status = Column(String) 
    reference_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    wallet = relationship("Wallet", back_populates="transactions")

class TransactionRequest(BaseModel):
    reference_id: str
    amount: int