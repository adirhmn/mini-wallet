from sqlalchemy.orm import Session
from models import Customer, Wallet, WalletRequestDisabled
from sqlalchemy.exc import SQLAlchemyError
from utils.exception import CustomHTTPException
from fastapi import status

class WalletService:
    def __init__(self, db: Session, customer: Customer):
        self.customer_xid = customer.customer_xid
        self.db = db
    
    def init_wallet(self) -> Wallet:
        try:
            exist_wallet = self.db.query(Wallet).filter(Wallet.owner == self.customer_xid).first()
            if exist_wallet:
                if exist_wallet.status == "enabled":
                    raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Already enabled"})
                exist_wallet.status = 'enabled'
                self.db.commit()
                self.db.refresh(exist_wallet)
                return exist_wallet
            
            new_wallet = Wallet(owner = self.customer_xid, status='enabled')
            self.db.add(new_wallet)
            self.db.commit()
            self.db.refresh(new_wallet)
            return new_wallet
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            self.db.rollback()  # Rollback transactions to ensure data integrity
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "Internal Server Error"})
    
    def disable_wallet(self, request: WalletRequestDisabled) -> Wallet:
        try:
            if not request.is_disabled:
                raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "is_disabled field must be true"})
            exist_wallet = self.db.query(Wallet).filter(Wallet.owner == self.customer_xid).first()
            if exist_wallet:
                if exist_wallet.status == "disabled":
                    raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Already disabled"})
                exist_wallet.status = 'disabled'
                self.db.commit()
                self.db.refresh(exist_wallet)
                return exist_wallet
            else:
                raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Wallet not registered"})
            
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            self.db.rollback()  # Rollback transactions to ensure data integrity
            raise CustomHTTPException(status_code=500, detail="Internal Server Error")
    
    def get_wallet(self) -> Wallet:
        exist_wallet = self.db.query(Wallet).filter(Wallet.owner == self.customer_xid).first()
        if not exist_wallet:
            raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Wallet not registered"})
        if exist_wallet.status == "disabled":
            raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Wallet disabled"})
        return exist_wallet