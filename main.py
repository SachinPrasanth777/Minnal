from fastapi import FastAPI
from utilities.database import Database

app = FastAPI()
settings = Database()

@app.get("/")
async def startup():
    return {"Hello World"}
