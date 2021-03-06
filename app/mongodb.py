import pymongo
import os
from hashlib import sha256
import jwt
from .config import *

class MongoDB:
    def __init__(self):
        self.db_pw = MONGODB_PASSWORD
        self.db_url = MONGODB_URL
        print(self.db_url.format(pw=str(self.db_pw)))
        self.client = pymongo.MongoClient(self.db_url.format(pw=str(self.db_pw)))
        self.db = self.client["test"]
        self.users = self.db["users"]
        self.preferences = self.db["pref"]
        self.misc = self.db["misc"]

    def register(self, username, pw, email):
        data = {
            "_id": username,
            "pwhash": sha256(pw.encode()).hexdigest(),
            'email':email
        }

        k = self.users.find_one({'_id': username})
        if not (k is None):
            return False, "User already registered!"
        d = self.users.insert_one(data)
        return d, 'Success!'

    def login(self, username, pw):
        u = self.users.find_one({'_id': username})
        if u is None:
            return False, "User not found!"
        phash = u['pwhash']
        if phash == sha256(pw.encode()).hexdigest():
            return True, "Success!"
        return False, "Password is incorrect!"

    def auth(self,jwt_token):
        decoded_jwt = jwt.decode(jwt_token, str(JWT_SECRET), JWT_ALGORITHM)
        res, username = self.validate(decoded_jwt)
        return res,username

    def validate(self,data):
        username = data["username"]
        k = self.users.find_one({'_id': username})
        if k is None:
            return False, "No user identification data in jwt!"
        return True, username