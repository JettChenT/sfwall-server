from fastapi import FastAPI, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from unsplash import Unsplash,make_unsplash
from data import DB
from datetime import datetime, timedelta
from config import *

app = FastAPI()
db = DB()

class RegisterINP(BaseModel):
    username: str
    email: str
    password: str


@app.get("/")
async def home():
    return {"msg": "Welcome!"}


@app.get("/ping")
async def pong():
    return {"ping": "pong"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def reg(inp: RegisterINP, response: Response):
    res, msg = db.register(inp.username, inp.password, inp.email)
    if not res:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"msg": msg}


@app.get("/login", status_code=status.HTTP_200_OK)
async def login(username, password, response: Response):
    res, msg = db.login(username, password)
    if not res:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": msg}
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(days=JWT_EXP_DAYS)
    }
    encoded_jwt = jwt.encode(payload, JWT_SECRET)
    return {"jwt": encoded_jwt}


@app.get("/random", status_code=status.HTTP_200_OK)
async def random_img(token, response: Response):
    try:
        decoded_jwt = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        res, msg = db.validate(decoded_jwt)
        if not res:
            raise Exception("No user data in jwt!")
        img_id = make_unsplash().get_random_img()
        return {"img_id": img_id}
    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg": str(e)}
