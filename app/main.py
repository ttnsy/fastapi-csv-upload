import json
import logging
import logging.config
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(
        f"{request.method} {request.url.path} completed in {process_time:.2f} ms"
    )
    return response


@app.get("/")
async def root():
    return {"message": "Welcome!"}


@app.get("/slow")
async def slow():
    time.sleep(2)
    return {"message": "Simulated slow endpoint for testing logging."}
