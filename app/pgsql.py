from fastapi import FastAPI
from databases import Database
import logging
from config import *

logger = logging.getLogger(__name__)

async def connect_to_db(app:FastAPI) -> None:
    database = Database(DATABASE_URL)
    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")

async def close_db_connection(app:FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")

