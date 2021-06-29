import time

from .config import *
from random import randint
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, insert, MetaData
from sqlalchemy.orm import declarative_base

UPPER = 24999
Base = declarative_base()
metadata = MetaData()


class PicDB:
    def __init__(self):
        self.db = create_engine(DATABASE_URL)

    def get_len(self, table):
        res = self.db.execute(f"SELECT COUNT(*) FROM {table}")
        rw = res.fetchall()
        return rw[0][0]

    def get_random_img(self):
        res = self.db.execute(f"SELECT photo_id FROM testphotos WHERE index={randint(0, UPPER)};")
        rw = res.fetchall()
        return rw[0][0]

    def get_n_random_img(self,n):
        res = self.db.execute(f"SELECT photo_id FROM testphotos TABLESAMPLE SYSTEM(0.3) WHERE index<{UPPER} LIMIT({n});")
        rw = res.fetchall()
        rw = [r[0] for r in rw]
        return rw

    def get_categories(self, img_id):
        res = self.db.execute(f"SELECT keyword FROM unsplash_keywords WHERE photo_id=\'{img_id}\';")
        rw = res.fetchall()
        return rw

    def add_rating(self, userid, imageid, rating):
        ratings_table = Table('user_ratings', metadata, autoload_with=self.db)
        stmt = (
            insert(ratings_table).
                values(user_id=userid, photo_id=imageid, rating=rating)
        )
        self.db.execute(stmt)