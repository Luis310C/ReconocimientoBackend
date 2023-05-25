from models import UserModel
from motor.motor_asyncio import AsyncIOMotorClient
from Services.CyptographyService import CryptographyService
import configparser


class UserService:
    __database_client: AsyncIOMotorClient = None
    __cryptography_context: CryptographyService = None

    def __init__(self, connection_string: str, symmetric_key_public: str):
        self.__cryptography_context = CryptographyService(symmetric_key_public)
        self.__database_client = AsyncIOMotorClient(self.__cryptography_context.
                                                    symmetric_decrypt(connection_string))

    async def authenticate(self, username, password):
        response = None
        cursor = await self.__database_client.json_collection. \
            find_one({"_id": username})
        if cursor:
            is_valid = self.__cryptography_context.verify_password(password, cursor["password"])
            if is_valid:
                response = self.__cryptography_context.create_access_token({"sub": username})
        return response

    async def create_user(self, user: UserModel):
        user_dict = user.dict()
        user_dict["_id"] = user_dict["username"]
        try:
            creation = await self.__database_client.test.test_collection.insert_one(user_dict)
        except:
            creation = None
        return {"success": "creation"}
