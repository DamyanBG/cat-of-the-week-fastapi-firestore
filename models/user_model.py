from pydantic import BaseModel, Field, EmailStr

from utils.enums import RoleType


class UserBase(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone_number: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: str
    role: RoleType = Field(...)
