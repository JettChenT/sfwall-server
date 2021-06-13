import time
import random

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from config import *

db = create_engine(DATABASE_URL)

class PicDB:
    def __init__(self):
        self.db = create_engine(DATABASE_URL)
    def get_len(self,table):
        res = self.db.execute(f"SELECT COUNT(*) FROM {table}")
        rw = res.fetchall()
        return rw[0][0]
    def load_data(self):
        file1 = open("./data/create_tables.sql")
        query1 = text(file1.read())
        self.db.execute(query1)
        file = open("./data/load_data.sql")
        query = text(file.read())
        self.db.execute(query)



def add_new_row(n):
    # Insert a new number into the 'numbers' table.
    db.execute("INSERT INTO temp3 (number,timestamp) "
        "VALUES ({0},{1})"
            .format(str(n), str(int(round(time.time() * 1000))))
    )


def get_last_row():
    # Retrieve the last number inserted inside the 'numbers'
    query = "" + \
            "SELECT number " + \
            "FROM temp3 " + \
            "WHERE timestamp >= (SELECT max(timestamp) FROM temp3)" + \
            "LIMIT 1"

    result_set = db.execute(query)
    for (r) in result_set:
        return r[0]

def init_tmp_table():
    sql_str = """
    CREATE TABLE IF NOT EXISTS temp3(
        number int,
        timestamp varchar(14)
    )
    """
    db.execute(sql_str)



def main():
    init_tmp_table()
    add_new_row(random.randint(1, 100000))
    return 'The last value insterted is: {}'.format(get_last_row())