import os
from .models import *
from .config import *
from .postgres import PicDB
from .ai import *

from fastapi import FastAPI, status, Depends, Security, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_auth0 import Auth0, Auth0User
from mangum import Mangum

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"
app = FastAPI(title="SFWALL API")
scopes = {
    "rate:images": "rate images"
}
auth = Auth0(domain=AUTH0_DOMAIN, api_audience=AUTH0_API_AUDIENCE, )

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
def random_img(response: Response, n: int = 1,  user: Auth0User = Security(auth.get_user)):
    resp,status_code = get_random_img(n)
    response.status_code = status_code
    return resp

@app.get("/similar", status_code=status.HTTP_200_OK, dependencies=[Depends(auth.implicit_scheme)])
def sim(img_id, n: int, response: Response, user: Auth0User = Security(auth.get_user)):
    resp, status_code = get_similar_images(img_id, n)
    response.status_code = status_code
    return resp

@app.post("/rate", status_code=status.HTTP_200_OK, dependencies=[Depends(auth.implicit_scheme)])
def rate(inp: RateINP, user: Auth0User = Security(auth.get_user)):
    pd = PicDB()
    pd.add_rating(user.id, inp.photo_id, inp.rating)
    return {"msg": "Success!"}

@app.get("/generatetoken", status_code=status.HTTP_200_OK, dependencies=[Depends(auth.implicit_scheme)])
def gen_token(user: Auth0User = Security(auth.get_user)):
    pd = PicDB()
    access_token = pd.gen_access_token(user.id)
    return {"access_token": access_token}

@app.post("/update",status_code=status.HTTP_200_OK, dependencies=[Depends(auth.implicit_scheme)])
def update_model(response:Response, user:Auth0User=Security(auth.get_user)):
    resp, code = update()
    response.status_code=code
    return resp


@app.get("/top", status_code=status.HTTP_200_OK, dependencies=[Depends(auth.implicit_scheme)])
def top(n:int, response:Response, user: Auth0User = Security(auth.get_user)):
    resp,code = get_top(user.id,n)
    response.status_code=code
    return resp


@app.get("/recommendation", status_code=status.HTTP_200_OK, dependencies=[Depends(auth.implicit_scheme)])
def recommend(response: Response, dtime:str='', user: Auth0User = Security(auth.get_user)):
    print(user)
    resp, code = get_recommendation(user.id,dtime=dtime)
    response.status_code = code
    return resp

@app.get("/token-recommendation", status_code=status.HTTP_200_OK)
def token_recommend(access_token,response: Response, dtime:str=''):
    pd = PicDB()
    user_id = pd.get_user_by_access_token(access_token)
    if user_id is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'msg': 'Invalid access token'}
    resp, code = get_recommendation(user_id, dtime=dtime)
    response.status_code = code
    return resp

handler = Mangum(app)