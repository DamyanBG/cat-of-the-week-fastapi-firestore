import jwt
from datetime import datetime, timedelta, UTC
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config import JWT_KEY
from models.user_model import User, UserId

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(user: User) -> str:
    payload = {
        "sub": user.id,
        "exp": datetime.now(UTC) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
        "role": user.role,
    }
    encoded_jwt = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> UserId:
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = UserId(id=user_id)
    except jwt.PyJWTError:
        raise credentials_exception
    return user_id


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserId:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)
