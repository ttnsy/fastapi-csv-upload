import json
import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import csv_file


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


with open("logging.json", "r") as f:
    config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


app = FastAPI(lifespan=lifespan)

app.include_router(csv_file.router)


@app.get("/")
async def root():
    return {"message": "Welcome!"}
