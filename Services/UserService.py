from models import UserModel
from motor.motor_asyncio import AsyncIOMotorClient
from Services.CyptographyService import CryptographyService
from Services.ServiceRecognize import ServiceRecognize
import configparser


class UserService:
    __database_client: AsyncIOMotorClient = None
    __cryptography_context: CryptographyService = None
    __database = None
    __recognize_service = None

    def __init__(self, connection_string: str, symmetric_key_public: str):
        self.__cryptography_context = CryptographyService(symmetric_key_public)
        self.__database_client = AsyncIOMotorClient(self.__cryptography_context.
                                                    symmetric_decrypt(connection_string))
        self.__database = self.__database_client.web_app
        self.__recognize_service = ServiceRecognize()

    async def authenticate(self, username, password):
        response = None
        cursor = await self.__database.users. \
            find_one({"_id": username})
        if cursor:
            is_valid = self.__cryptography_context.verify_password(password, cursor["password"])
            if is_valid:
                response = self.__cryptography_context.create_access_token({"sub": username})
        return response

    async def create_user(self, user: UserModel):
        user_dict = user.dict()
        user_dict["_id"] = user_dict["username"]
        user_dict["password"] = self.__cryptography_context.get_password_hash(user_dict["password"])
        try:
            creation = await self.__database.users.insert_one(user_dict)
        except:
            creation = None
        return {"success": "creation"}
