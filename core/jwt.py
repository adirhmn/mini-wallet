from typing import Optional
from fastapi import status
import core.config as config
from sqlalchemy.orm import Session
import jwt
from jwt import PyJWTError
from fastapi import Depends
from datetime import datetime, timedelta
from db.session import get_db
from models import Customer, TokenPayload
from utils.exception import CustomHTTPException
from .schema_auth import OAuth2Token

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    # create jwt access token.
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2Token(tokenUrl="token")

async def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[Customer]:
    # Verify the JWT token and get the current user.

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError as e:
        error_message = str(e)
        raise CustomHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_message)
    
    customer = db.query(Customer).filter(Customer.customer_xid == token_data.sub).first()
    if not customer:
        raise CustomHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return customer