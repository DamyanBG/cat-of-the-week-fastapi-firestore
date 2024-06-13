from pydantic import BaseModel


class LoginRequestModel(BaseModel):
    email: str
    password: str


class LoginResponseModel(BaseModel):
    token: str
