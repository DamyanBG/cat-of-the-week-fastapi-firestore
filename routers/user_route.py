from fastapi import APIRouter, HTTPException, status

from models.user_model import User, UserCreate
from models.login_model import LoginRequestModel, LoginResponseModel
from auth.password import hash_password, check_hashed_password
from auth.token import create_access_token
from queries.user_queries import select_user_by_email, insert_user
from queries.cat_queries import select_cat_by_user_id

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/register", response_model=User)
async def create_user(user: UserCreate):
    existing_user = await select_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered!"
        )

    user.password = hash_password(user.password)
    new_user = await insert_user(user)

    return new_user


@user_router.post("/login", response_model=LoginResponseModel)
async def login_user(credentials: LoginRequestModel):
    existing_user = await select_user_by_email(credentials.email)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad credentials!"
        )

    if not check_hashed_password(existing_user.password, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad credentials!"
        )

    token = create_access_token(existing_user)
    user_cat = await select_cat_by_user_id(existing_user.id)

    has_uploaded_cat = bool(user_cat)

    return {"token": token, "has_uploaded_cat": has_uploaded_cat}
