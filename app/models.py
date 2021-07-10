from pydantic import BaseModel


class RegisterINP(BaseModel):
    username: str
    email: str
    password: str

class RateINP(BaseModel):
    rating:float
    photo_id:str