import requests
from .config import AI_API_KEY

def get_similar_images(img_id, n):
    r = requests.get(
        "https://ai.scan4wall.xyz/similar", {
            "img_id": img_id,
            "cnt": n,
            "access_token": AI_API_KEY
        })
    r_data = r.json()
    return r_data, r.status_code

def get_recommendation(user_id, dtime=''):
    r = requests.get(
        "https://ai.scan4wall.xyz/recommend", {
            "user_id":user_id,
            "dtime":dtime,
            "access_token": AI_API_KEY
        }
    )
    r_data = r.json()
    return r_data, r.status_code

def get_top(user_id, n):
    r = requests.get(
        "https://ai.scan4wall.xyz/top", {
            "user_id":user_id,
            "n":n,
            "access_token":AI_API_KEY
        }
    )
    r_data = r.json()
    return r_data, r.status_code

def update():
    r = requests.post(
        f"https://ai.scan4wall.xyz/update?access_token={AI_API_KEY}"
    )
    r_data = r.json()
    return r_data, r.status_code

def get_random_img(n):
    r = requests.get(
        "https://ai.scan4wall.xyz/random",{
            "n":n
        }
    )
    r_data = r.json()
    return r_data, r.status_code