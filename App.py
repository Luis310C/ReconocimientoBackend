import tempfile

from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Tuple
from fastapi import FastAPI, Body, HTTPException, UploadFile, File, Form, Request
from fastapi.encoders import jsonable_encoder
import configparser

from Services.UserService import UserService

from models import UserModel, LoginRequestModel, LoginRequestBase64Model, DpiModel

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=100)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
config = configparser.ConfigParser()
config.read('config.ini')
connection = config["CONNECTIONS"]["mongo_connection_string"]
public_key = config["CONNECTIONS"]["public_key"]
user_service = UserService(connection, public_key,
                           config_whatsapp=config["WHATSAPP"], config_email=config["EMAIL"])

app.add_event_handler('startup', user_service.start)
app.add_event_handler('shutdown', user_service.close)


def set_values(form_content):
    user_model: UserModel = UserModel()
    user_model.username = form_content["username"]
    user_model.password = form_content["password"]
    user_model.email = form_content["email"]
    user_model.phone = form_content["phone"]
    user_model.name = form_content["name"]
    user_model.last_name = form_content["last_name"]
    return user_model


@app.get('/')
async def root():
    return {'status': 200}


# @app.post('/user/create')
# async def create_user(user: UserModel):
#     return await user_service.create_user(user)


@app.post('/image/upload_image')
async def post_image(file: UploadFile = File(...)):
    content: bytes = file.file.read()
    token = await user_service.authenticate_face("vivian26", content)
    return {"filename": file.filename, "auth": token}


@app.post('/video/upload_video')
async def post_video(request: Request
                     , file: UploadFile = File(...)):
    file_bytes = await file.read()
    response = ""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_bytes)
        temp_file_path = temp_file.name
        form_content = await request.form()
        model = set_values(form_content)
        response = await user_service.create_user(model, temp_file_path)
    return response


@app.post('/login/image')
async def login_image(file: UploadFile = File(...)):
    file_bytes = await file.read()
    return user_service.authenticate_face("jose310", file_bytes)


@app.post('/login/base64')
async def login_base64(user: LoginRequestBase64Model):
    return await user_service.authenticate_base64(user.username, user.image_base64)


@app.post('/login')
async def login(user: LoginRequestModel):
    return await user_service.authenticate(user.username, user.password)


@app.post('/validate/dpi')
async def validate_dpi(dpi: DpiModel):
    return await user_service.validate_dpi(dpi)
