import jwt
from datetime import datetime, timedelta, UTC

from config import JWT_KEY
from models.user_model import User

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


def create_access_token(user: User) -> str:
    payload = {
        "sub": user.id,
        "exp": datetime.now(UTC) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
        "role": user.role,
    }
    encoded_jwt = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt
