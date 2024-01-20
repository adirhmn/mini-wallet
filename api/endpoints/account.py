from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from models import CustomerInit, SuccessResponse
from services.customer_service import CustomerService
from core.jwt import create_access_token

router = APIRouter()

@router.post("/init", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def init_customer(customer: CustomerInit, db: Session = Depends(get_db)):
    customer = CustomerService(db, customer).init_account()
    token = create_access_token(data={"sub": customer.customer_xid})
    return SuccessResponse(data={"token":token})