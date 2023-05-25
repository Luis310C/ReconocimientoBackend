from pydantic import BaseModel


class UserModel(BaseModel):
    username: str = None
    password: str = None
    email: str = None
    phone: str = None
    name: str = None
    last_name: str = None
    binary_image: bytes = None
    image_model: str = None
