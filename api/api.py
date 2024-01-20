from fastapi import APIRouter
from api.endpoints import account, wallet, base

api_router = APIRouter()
api_router.include_router(base.router, tags=["base"])
api_router.include_router(account.router, prefix="/api/v1", tags=["init"])
api_router.include_router(wallet.router, prefix="/api/v1/wallet", tags=["wallet"])