import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from db.session import Base
from datetime import datetime
from pydantic import BaseModel

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True, unique=True)
    owner = Column(String, ForeignKey('customers.customer_xid')) 
    status = Column(String, default='disabled')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet")

    def get_balance(self):
        # Calculate balance based on successful transactions
        deposit_amount = sum(transaction.amount for transaction in self.transactions if transaction.transaction_type == 'deposit' and transaction.status == 'success')
        withdrawal_amount = sum(transaction.amount for transaction in self.transactions if transaction.transaction_type == 'withdrawal' and transaction.status == 'success')
        balance = deposit_amount - withdrawal_amount
        return balance

class WalletRequestDisabled(BaseModel):
    is_disabled: bool
