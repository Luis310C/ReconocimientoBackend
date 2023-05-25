from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Tuple
from fastapi import FastAPI, Body, HTTPException, UploadFile, File, Form, Request
from fastapi.encoders import jsonable_encoder
import configparser

from Services.UserService import UserService

from models import UserModel, LoginRequestModel

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
    return {"filename": file.filename}


@app.post('/video/upload_video')
async def post_video(request: Request
                     , file: UploadFile = File(...)):
    file_bytes = await file.read()
    form_content = await request.form()
    model = set_values(form_content)
    return await user_service.create_user(model, file)


@app.post('/login/image')
async def login_image(request: Request, file: UploadFile = File(...)):
    file_bytes = await file.read()
    form_content = await request.form()
    return user_service.authenticate_face(form_content["username"], file_bytes)


@app.post('/login')
async def login(user: LoginRequestModel):
    return await user_service.authenticate(user.username, user.password)
