import jwt
from datetime import datetime, timedelta, UTC

from config import JWT_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


def create_access_token(user):
    payload = {
        "sub": user.pk,
        "exp": datetime.now(UTC) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
        "role": user.role,
    }
    encoded_jwt = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt
