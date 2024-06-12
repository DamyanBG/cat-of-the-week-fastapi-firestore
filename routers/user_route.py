import jwt
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta

from db import db
from utils.enums import RoleType
from models.user_model import User, UserCreate

user_router = APIRouter(prefix="/users", tags=["users"])

user_ref = db.collection("Users")

# Secret key for JWT encoding/decoding
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@user_router.post("/register-participant", response_model=User)
async def create_user(user: UserCreate):
    existing_users = user_ref.where("email", "==", user.email).get()
    if existing_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered!"
        )
    new_user_ref = user_ref.document()
    user_data = user.model_dump(by_alias=True, exclude_unset=True)
    user_data["role"] = RoleType.participant
    new_user_ref.set(user_data)
    user_data["id"] = new_user_ref.id

    # Generate JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return user_data
