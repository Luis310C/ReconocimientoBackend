from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Tuple
from fastapi import FastAPI, Body, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder
import configparser

from Services.UserService import UserService
from models import UserModel

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
user_service = UserService(connection, public_key)


@app.get('/')
async def root():
    return {'status': 200}


@app.post('/user/create')
async def create_user(user: UserModel):
    return await user_service.create_user(user)


@app.post('image/upload_image')
async def post_image(file: UploadFile = File(...)):
    content: bytes = file.file.read()
    return {"filename": file.filename}


@app.post('video/upload_video')
async def post_video(file: UploadFile = File(...)):
    content: bytes = file.file.read()
    return {"filename": file.filename}
