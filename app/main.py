from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import csv_file


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(csv_file.router)


@app.get("/")
async def root():
    return {"message": "Welcome!"}
