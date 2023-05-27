from pydantic import BaseModel


class LoginRequestModel(BaseModel):
    username: str = None
    password: str = None


class LoginRequestBase64Model(BaseModel):
    username: str = None
    image_base64: str = None


class UserModel(BaseModel):
    username: str = None
    password: str = None
    email: str = None
    phone: str = None
    name: str = None
    last_name: str = None
    model_name: str = None


class DpiModel(BaseModel):
    username: str = None
    back_dpi: str = None
    front_dpi: str = None
