from passlib.context import CryptContext
import configparser
from typing import Final
import cryptocode
import jwt


class CryptographyService:
    __password_context: CryptContext = None
    __symmetric_key_public: str = None
    __ALGORITHM: Final = "bcrypt"
    __JWT_ALGORITHM: Final = "HS256"

    def __init__(self, symmetric_key_public: str):
        self.__password_context = CryptContext(schemes=[self.__ALGORITHM], deprecated="auto")
        self.__symmetric_key_public = symmetric_key_public

    def get_password_hash(self, password: str) -> str:
        return self.__password_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.__password_context.verify(plain_password, hashed_password)

    def symmetric_encrypt(self, text: str) -> str:
        return cryptocode.encrypt(text, self.__symmetric_key_public)

    def symmetric_decrypt(self, text: str) -> str:
        return cryptocode.decrypt(text, self.__symmetric_key_public)

    def create_access_token(self, data: dict) -> str:
        return jwt.encode(data.copy(), self.__symmetric_key_public, algorithm=self.__JWT_ALGORITHM)
