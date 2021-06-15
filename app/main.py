from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import jwt
from unsplash import make_unsplash
from config import *
from .routers import users

app = FastAPI(title="Scan for wallpapers API")


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

app.include_router(users.router)


@app.get("/random", status_code=status.HTTP_200_OK)
def random_img(token, response: Response):
    try:
        decoded_jwt = jwt.decode(token, str(JWT_SECRET), JWT_ALGORITHM)
        res, msg = db.validate(decoded_jwt)
        if not res:
            raise Exception("No user data in jwt!")
        img_id = make_unsplash().get_random_img()
        return {"img_id": img_id}
    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg": str(e)}


@app.get("/testdb", status_code=status.HTTP_200_OK)
def testdb(response: Response):
    try:
        import postgres
        res = postgres.main()
        return {"msg": res}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorc": str(e)}


@app.get("/numrows", status_code=status.HTTP_200_OK)
def numrow(db_name, response: Response):
    try:
        from postgres import PicDB
        pd = PicDB()
        ln = pd.get_len(db_name)
        return {"len": ln}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}

@app.get("/createdb",status_code=status.HTTP_200_OK)
def createdb(response:Response):
    try:
        from postgres import PicDB
        pd = PicDB()
        pd.load_data()
        return {"msg": "success"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error":str(e)}

@app.get("/tosql",status_code=status.HTTP_200_OK)
def tosql(response:Response):
    try:
        from postgres import PicDB
        pd = PicDB()
        unsp = make_unsplash()
        unsp.to_sql(pd.db)
        return {"msg":"success"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
