from models import UserModel
from motor.motor_asyncio import AsyncIOMotorClient
from Services.CyptographyService import CryptographyService
from Services.ServiceRecognize import ServiceRecognize
from Services.NotificationService import NotificationService, StandardMessage
import configparser
import base64


class UserService:
    __database_client: AsyncIOMotorClient = None
    __cryptography_context: CryptographyService = None
    __database = None
    __recognize_service = None
    __notification_service = None

    def __init__(self, connection_string: str, symmetric_key_public: str,
                 config_whatsapp: configparser.SectionProxy, config_email: configparser.SectionProxy):
        self.__cryptography_context = CryptographyService(symmetric_key_public)
        self.__database_client = AsyncIOMotorClient(self.__cryptography_context.
                                                    symmetric_decrypt(connection_string))
        self.__database = self.__database_client.web_app
        self.__recognize_service = ServiceRecognize()
        config_email["smtp_password"] = self.__cryptography_context. \
            symmetric_decrypt(config_email["smtp_password"])
        self.__notification_service = NotificationService(config_email=config_email,
                                                          config_whatsapp=config_whatsapp)

    async def start(self):
        await self.__notification_service.start()

    async def close(self):
        await self.__notification_service.stop()
        self.__database_client.close()

    async def authenticate(self, username, password):
        response = None
        cursor = await self.__database.users. \
            find_one({"_id": username})
        if cursor:
            is_valid = self.__cryptography_context.verify_password(password, cursor["password"])
            if is_valid:
                response = self.__cryptography_context.create_access_token({"sub": username})
        return response

    async def authenticate_base64(self, username, image_base64):
        bytes_image = base64.b64decode(image_base64)
        return await self.authenticate_face(username, bytes_image)

    async def authenticate_face(self, username, face_bytes: bytes):
        response = None
        cursor = await self.__database.users. \
            find_one({"_id": username})
        if cursor:
            is_valid = self.__recognize_service.find_match(cursor["model_name"], face_bytes)
            if is_valid:
                response = self.__cryptography_context.create_access_token({"sub": username})
        return response

    async def create_user(self, user: UserModel, file):
        user.model_name = self.__recognize_service.get_faces(file.file.name, user.username)
        user_dict = user.dict()
        user_dict["_id"] = user_dict["username"]
        user_dict["password"] = self.__cryptography_context.get_password_hash(user_dict["password"])
        try:
            creation = await self.__database.users.insert_one(user_dict)
            message = StandardMessage()
            message.number_phone = user.phone
            message.email_address = user.email
            message.subject = "Registro exitoso"
            message.body = f"Estimado {user.name} {user.last_name}, su registro ha sido exitoso"
            await self.__notification_service.send_mail(message)
        except Exception as e:
            print(e)
            creation = None
        return {"success": "creation"}
