from pydantic import BaseModel


class RegisterINP(BaseModel):
    username: str
    email: str
    password: str

class RateINP(BaseModel):
    jwt:str
    rating:int
    photo_id:str