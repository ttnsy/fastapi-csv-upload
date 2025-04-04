from fastapi import FastAPI

from .routers import csv_file

app = FastAPI()

app.include_router(csv_file.router)


@app.get("/")
async def root():
    return {"message": "Welcome!"}
