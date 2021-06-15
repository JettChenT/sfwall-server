from datetime import datetime, timedelta
import jwt
from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from ..config import *
from ..mongodb import MongoDB

db = MongoDB()
router = APIRouter(tags=["user"])


class RegisterINP(BaseModel):
    username: str
    email: str
    password: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
def reg(inp: RegisterINP, response: Response):
    res, msg = db.register(inp.username, inp.password, inp.email)
    if not res:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"msg": msg}


@router.get("/login", status_code=status.HTTP_200_OK)
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
