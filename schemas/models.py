from pydantic import BaseModel
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Postgres(BaseModel):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str

@lru_cache
def database() -> Postgres:
    return Postgres(
        DB_USERNAME=os.getenv("DB_USERNAME"),
        DB_PASSWORD=os.getenv("DB_PASSWORD"),
        DB_NAME=os.getenv("DB_NAME")
    )