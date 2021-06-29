import os
from .models import *
from .config import *
from .mongodb import MongoDB
from .postgres import PicDB

from fastapi import FastAPI, status, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi_auth0 import Auth0, Auth0User
from mangum import Mangum

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"
app = FastAPI(title="SFWALL API")
db = MongoDB()
scopes = {
    "rate:images":"rate images"
}
auth = Auth0(domain=AUTH0_DOMAIN, api_audience=AUTH0_API_AUDIENCE,)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"msg": "Welcome!"}


@app.get("/pingpong")
async def pong():
    return {"ping": "pong"}

@app.get("/random", status_code=status.HTTP_200_OK, dependencies=[Depends(auth.implicit_scheme)])
def random_img(n:int =1):
    pd = PicDB()
    if n==1:
        img_id = pd.get_random_img()
        return {"img_id": img_id}
    elif n>10:
        return {"detail": "Requesting too many images"}
    else:
        res = pd.get_n_random_img(n)
        return {"length":n,"result":[{"img_id":img_id} for img_id in res]}

@app.post("/rate", status_code=status.HTTP_200_OK, dependencies=[Depends(auth.implicit_scheme)])
def rate(inp: RateINP, user: Auth0User = Security(auth.get_user)):
    pd = PicDB()
    pd.add_rating(user.id, inp.photo_id, inp.rating)
    return {"msg":"Success!"}

handler = Mangum(app)