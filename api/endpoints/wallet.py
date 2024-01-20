from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from models import Customer, SuccessResponse, TransactionRequest, WalletRequestDisabled
from services.wallet_service import WalletService
from services.transaction_service import TransactionService
from core.jwt import get_current_customer
from utils.utils import formatted_datetime

router = APIRouter()

@router.post("/", status_code = status.HTTP_201_CREATED)
def init_wallet(db: Session = Depends(get_db), current_customer: Customer = Depends(get_current_customer)):
    wallet = WalletService(db, current_customer).init_wallet()
    response = {
        "wallet": {
            "id": wallet.id,
            "owned_by": wallet.owner,
            "status": wallet.status,
            "enabled_at": formatted_datetime(wallet.updated_at),
            "balance": wallet.get_balance()
        }
    }
    return SuccessResponse(data=response)

@router.get("/")
def view_wallet(db: Session = Depends(get_db), current_customer: Customer = Depends(get_current_customer)):
    wallet = WalletService(db, current_customer).get_wallet()
    response = {
        "wallet": {
            "id": wallet.id,
            "owned_by": wallet.owner,
            "status": wallet.status,
            "enabled_at": formatted_datetime(wallet.updated_at),
            "balance": wallet.get_balance()
        }
    }
    return SuccessResponse(data=response)

@router.patch("/")
def disable_wallet(request: WalletRequestDisabled ,db: Session = Depends(get_db), 
                   current_customer: Customer = Depends(get_current_customer)):
    wallet = WalletService(db, current_customer).disable_wallet(request)
    response = {
        "wallet": {
            "id": wallet.id,
            "owned_by": wallet.owner,
            "status": wallet.status,
            "disabled_at": formatted_datetime(wallet.updated_at),
            "balance": wallet.get_balance()
        }
    }
    return SuccessResponse(data=response)

@router.get("/transactions")
def view_transactions(db: Session = Depends(get_db), current_customer: Customer = Depends(get_current_customer)):
    transactions = TransactionService(db, current_customer).get_transactions()
    data_transactions = []
    for transaction in transactions:
        data = {
            "id": transaction.id,
            "status": transaction.status,
            "transacted_at": formatted_datetime(transaction.created_at),
            "type": transaction.transaction_type,
            "amount": transaction.amount,
            "reference_id": transaction.reference_id
        }
        data_transactions.append(data)
    response = {
        "transactions":data_transactions
    }
    return SuccessResponse(data=response)

@router.post("/deposits", status_code = status.HTTP_201_CREATED)
def add_money(request: TransactionRequest, db: Session = Depends(get_db), current_customer: Customer = Depends(get_current_customer)):
    deposit = TransactionService(db, current_customer).insert_deposit(request)
    response = {
        "deposit": {
            "id": deposit.id,
            "deposited_by": current_customer.customer_xid,
            "status": deposit.status,
            "deposited_at": formatted_datetime(deposit.created_at),
            "amount": deposit.amount,
            "reference_id": deposit.reference_id
        }
    }
    return SuccessResponse(data=response)

@router.post("/withdrawals", status_code = status.HTTP_201_CREATED)
def use_money(request: TransactionRequest, db: Session = Depends(get_db), current_customer: Customer = Depends(get_current_customer)):
    deposit = TransactionService(db, current_customer).insert_withdrawal(request)
    response = {
        "deposit": {
            "id": deposit.id,
            "withdrawn_by_by": current_customer.customer_xid,
            "status": deposit.status,
            "withdrawn_by_at": formatted_datetime(deposit.created_at),
            "amount": deposit.amount,
            "reference_id": deposit.reference_id
        }
    }
    return SuccessResponse(data=response)
