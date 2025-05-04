from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from .database import engine
from .routers import csv_file


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(csv_file.router)


@app.get("/")
async def root():
    return {"message": "Welcome!"}
