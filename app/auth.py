from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.schemas import TokenData
from app import models, database
from app.custom_exceptions.exceptions import (custom_exception_from_jwt,
custom_token_available_exception)

from .config import settings

security = HTTPBearer(auto_error=False)

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


def verify_token(token: str, credentials_exception):
    """Verify JWT token and return the token data."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = str(payload.get("user_id"))
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError as exc:
        raise credentials_exception from exc
    return token_data


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(database.get_db)):
    token_exception = custom_token_available_exception()
    credentials_exception = custom_exception_from_jwt()
    if not credentials:
        raise token_exception
    token = credentials.credentials
    token_data = verify_token(token, credentials_exception)
    user = db.get(models.User, token_data.id)
    if user is None:
        raise credentials_exception
    return user