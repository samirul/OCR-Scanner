from uuid import UUID
from fastapi import status, HTTPException

def custom_token_available_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication Credential is not provided.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def custom_exception_from_jwt():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

def check_valid_uuid(ids: str):
    try:
        UUID(ids)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format.",
        ) from e