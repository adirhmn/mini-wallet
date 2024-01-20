from sqlalchemy.orm import Session
from models import Customer, Wallet, Transaction, TransactionRequest
from sqlalchemy import desc
from utils.exception import CustomHTTPException
from fastapi import status

class TransactionService:
    def __init__(self, db: Session, customer: Customer):
        self.customer_xid = customer.customer_xid
        self.db = db
        self.transaction_type = ['deposit', 'withdrawal']

    def get_transactions(self) -> [Transaction]:
        exist_wallet = self.check_existing_wallet()
        wallet_id = exist_wallet.id
        transactions = self.db.query(Transaction).filter(Transaction.wallet_id == wallet_id).order_by(desc(Transaction.created_at)).all()
        return transactions
    
    def insert_deposit(self, transaction: TransactionRequest) -> Transaction:
        exist_wallet = self.check_existing_wallet()
        exist_transaction = self.db.query(Transaction)\
                    .filter(Transaction.reference_id == transaction.reference_id)\
                    .first()
        if exist_transaction:
            raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Transaction with this reference_id already added"})
        wallet_id = exist_wallet.id
        err_amount, is_valid_amount = self.validate_amount(transaction.amount)
        new_transaction = Transaction(wallet_id=wallet_id, amount=transaction.amount, 
                                      transaction_type=self.transaction_type[0], 
                                      status="success" if is_valid_amount else "failed",
                                      reference_id=transaction.reference_id)
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(new_transaction)
        if err_amount:
            raise err_amount
        return new_transaction

    def insert_withdrawal(self, transaction: TransactionRequest) -> Transaction:
        exist_wallet = self.check_existing_wallet()
        exist_transaction = self.db.query(Transaction)\
                    .filter(Transaction.reference_id == transaction.reference_id)\
                    .first()
        if exist_transaction:
            raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Transaction with this reference_id already added"})
        wallet_id = exist_wallet.id
        err_amount, is_valid_amount = self.validate_amount(transaction.amount)
        err_withdraw, is_valid_withdraw = self.validate_withdrawal(exist_wallet, transaction.amount)
        new_transaction = Transaction(wallet_id=wallet_id, amount=transaction.amount, 
                                      transaction_type=self.transaction_type[1], 
                                      status="success" if is_valid_amount and is_valid_withdraw else "failed",
                                      reference_id=transaction.reference_id)
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(new_transaction)
        if err_amount:
            raise err_amount
        if err_withdraw:
            raise err_withdraw
        return new_transaction
    
    def check_existing_wallet(self) -> Wallet:
        exist_wallet = self.db.query(Wallet).filter(Wallet.owner == self.customer_xid).first()
        if not exist_wallet:
            raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Wallet not registered"})
        if exist_wallet.status == "disabled":
            raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Wallet disabled"})
        return exist_wallet
    
    def validate_amount(self, transaction_amount: int) -> (any, bool):
        if transaction_amount <= 0:
            error = CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Amount must be higher than 0"})
            return error, False
        return None, True
    
    def validate_withdrawal(self, wallet: Wallet,transaction_amount: int) -> (any, bool):
        current_balance = wallet.get_balance()
        if transaction_amount > current_balance:
            error = CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Balance is not enough"})
            return error, False
        return None, True
        