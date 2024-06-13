
from fastapi import APIRouter, HTTPException, status


from db import db
from utils.enums import RoleType
from models.user_model import User, UserCreate
from models.login_model import LoginRequestModel, LoginResponseModel

user_router = APIRouter(prefix="/users", tags=["users"])

user_ref = db.collection("Users")



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
    
    return user_data


@user_router.post("/login", response_model=LoginResponseModel)
async def login_user(credentials: LoginRequestModel):
    existing_users = user_ref.where("email", "==", credentials.email).get()
    if not existing_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad credentials!"
        )
    
    user = existing_users[0]
    
