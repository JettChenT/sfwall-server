from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config()

MONGODB_PASSWORD = config("MONGODB_PASSWORD", cast=Secret)
MONGODB_URL = config("MONGODB_URL", cast=str)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str)
JWT_EXP_DAYS = config("JWT_EXP_DAYS", cast=int)
JWT_SECRET = config("JWT_SECRET", cast=Secret)
POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)
AUTH0_API_AUDIENCE = config("AUTH0_API_AUDIENCE",cast=str)
AUTH0_DOMAIN = config("AUTH0_DOMAIN",cast=str)
DATABASE_URL = config(
    "DATABASE_URL",
    cast=str,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
