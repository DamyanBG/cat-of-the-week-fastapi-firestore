from fastapi import APIRouter, HTTPException, status
from google.cloud.firestore import FieldFilter

from db import db
from utils.enums import RoleType
from models.user_model import User, UserCreate
from models.login_model import LoginRequestModel, LoginResponseModel
from auth.password import hash_password, check_hashed_password
from auth.token import create_access_token

user_router = APIRouter(prefix="/users", tags=["users"])

user_ref = db.collection("Users")


@user_router.post("/register", response_model=User)
async def create_user(user: UserCreate):
    existing_users = user_ref.where("email", "==", user.email).get()
    if existing_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered!"
        )
    new_user_ref = user_ref.document()
    user.password = hash_password(user.password)
    user_data = user.model_dump(by_alias=True, exclude_unset=True)
    user_data["role"] = RoleType.user
    new_user_ref.set(user_data)
    user_data["id"] = new_user_ref.id

    return user_data


@user_router.post("/login", response_model=LoginResponseModel)
async def login_user(credentials: LoginRequestModel):
    field_filter = FieldFilter("email", "==", credentials.email)
    existing_users = user_ref.where(filter=field_filter).get()
    if not existing_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad credentials!"
        )

    user_doc = existing_users[0]
    user_dict = user_doc.to_dict()
    user_dict["id"] = user_doc.id
    user = User(**user_dict)

    if not check_hashed_password(user.password, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad credentials!"
        )

    token = create_access_token(user)

    return {"token": token}
