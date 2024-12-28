from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def startup():
    return {"Hello World"}
