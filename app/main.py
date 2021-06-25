import os
from .models import *
from .config import *
from .mongodb import MongoDB
from .postgres import PicDB

from fastapi import FastAPI, Response, status
import jwt
from datetime import datetime, timedelta
from mangum import Mangum

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"
app = FastAPI(title="SFWALL API")
db = MongoDB()

@app.get("/")
async def home():
    return {"msg": "Welcome!"}


@app.get("/ping")
async def pong():
    return {"ping": "pong"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
def reg(inp: RegisterINP, response: Response):
    res, msg = db.register(inp.username, inp.password, inp.email)
    if not res:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"msg": msg}


@app.get("/login", status_code=status.HTTP_200_OK)
def login(username, password, response: Response):
    res, msg = db.login(username, password)
    if not res:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": msg}
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(days=JWT_EXP_DAYS)
    }
    encoded_jwt = jwt.encode(payload, str(JWT_SECRET))
    return {"jwt": encoded_jwt}


@app.get("/random", status_code=status.HTTP_200_OK)
def random_img(token, response: Response):
    try:
        res, msg = db.auth(token)
        if not res:
            raise Exception("No user data in jwt!")
        pd = PicDB()
        img_id = pd.get_random_img()
        return {"img_id": img_id}
    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": str(e)}

@app.post("/rate", status_code=status.HTTP_200_OK)
def rate(inp: RateINP, response:Response):
    try:
        res, msg = db.auth(inp.jwt)
        if not res:
            raise Exception(msg)
        pd = PicDB()
        username = msg
        pd.add_rating(username,inp.photo_id,inp.rating)
        return {"msg":"Success!"}
    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": str(e)}

handler = Mangum(app)