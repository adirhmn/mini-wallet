from sqlalchemy.orm import Session
from fastapi import status
from models import Customer, CustomerInit
from sqlalchemy.exc import SQLAlchemyError
from utils.exception import CustomHTTPException

class CustomerService:
    def __init__(self, db: Session, customer: CustomerInit):
        self.customer = customer
        self.db = db
    
    def init_account(self) -> Customer:
        try:
            exist_customer = self.db.query(Customer).filter(Customer.customer_xid == self.customer.customer_xid).first()
            if exist_customer:
                return exist_customer
            new_customer = Customer(customer_xid = self.customer.customer_xid)
            self.db.add(new_customer)
            self.db.commit()
            self.db.refresh(new_customer)

            return new_customer
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            self.db.rollback()  # Rollback transactions to ensure data integrity
            raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "Internal Server Error"})
