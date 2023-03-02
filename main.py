from fastapi import FastAPI
from Scheduler import Scheduler

app = FastAPI()

scheduler = Scheduler()


@app.get("/")
async def root():
    return {"message": "Hello World"}