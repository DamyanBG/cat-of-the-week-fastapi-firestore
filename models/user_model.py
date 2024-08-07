from pydantic import BaseModel, Field, EmailStr

from utils.enums import RoleType


class UserBase(BaseModel):
    first_name: str = Field(
        ..., max_length=100, description="First name of the user", example="John"
    )
    last_name: str = Field(
        ..., max_length=100, description="Last name of the user", example="Doe"
    )
    email: EmailStr = Field(...)
    password: str = Field(...)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserId(BaseModel):
    id: str


class User(UserBase):
    id: str
    role: RoleType = Field(...)
