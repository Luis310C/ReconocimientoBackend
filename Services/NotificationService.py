from configparser import SectionProxy

from aiohttp import ClientSession
from aiosmtplib import SMTP
from email.message import EmailMessage


class StandardMessage:
    number_phone: str = None
    body: str = None
    email_address: str = None
    subject: str = None


class NotificationService:
    __smtp_client: SMTP = None
    __config_email: SectionProxy = None
    __whatsapp_client: ClientSession = None
    __whatsapp_headers: dict = {}
    __whatsapp_url: str = None

    def __init__(self, config_email: SectionProxy, config_whatsapp: SectionProxy):
        self.__config_email = config_email
        self.__whatsapp_headers = {
            'Authorization': f'Bearer {config_whatsapp["access_token"]}',
            'Content-Type': 'application/json'
        }
        self.__whatsapp_url = config_whatsapp["url"]
        self.__whatsapp_client = ClientSession()
        self.__smtp_client = SMTP(hostname=config_email["smtp_server"],
                                  username=config_email["smtp_user"],
                                  password=config_email["smtp_password"],
                                  port=587)

    async def start(self):
        await self.__smtp_client.connect()

    async def send_mail(self, message_content: StandardMessage):
        message = EmailMessage()
        message["From"] = self.__config_email["smtp_user"]
        message["To"] = message_content.email_address
        message["Subject"] = message_content.subject
        message.set_content(message_content.body)
        await self.__smtp_client.send_message(message)

    async def stop(self):
        await self.__smtp_client.quit()
        await self.__whatsapp_client.close()

    async def send_message(self, message_content: StandardMessage):
        payload = {
            "messaging_product": "whatsapp",
            "to": f"+502{message_content.number_phone}",
            "type": "template",
            "template": {
                "name": message_content.body,
                "language": {
                    "code": "en_US"
                }
            }
        }
        response = await self.__whatsapp_client.post(url=self.__whatsapp_url,
                                                     json=payload, headers=self.__whatsapp_headers)
        print(await response.text())