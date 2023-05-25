from pydantic import BaseModel


class LoginRequestModel(BaseModel):
    username: str = None
    password: str = None


class UserModel(BaseModel):
    username: str = None
    password: str = None
    email: str = None
    phone: str = None
    name: str = None
    last_name: str = None
    model_name: str = None
