import pymongo
import os
from hashlib import sha256

class DB:
    def __init__(self):
        self.db_url = os.getenv("DB_URL")
        self.db_pw = os.getenv("DB_PASSWORD")
        print(self.db_url.format(pw=self.db_pw))
        self.client = pymongo.MongoClient(self.db_url.format(pw=self.db_pw))
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

    def validate(self,data):
        username = data["username"]
        k = self.users.find_one({'_id': username})
        if k is None:
            return False, "No user identification data in jwt!"
        return True, "authorized!"