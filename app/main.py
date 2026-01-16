import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.log_config import logger_telemetry
from app.routers import analysis, csv_file


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(csv_file.router)
app.include_router(analysis.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger_telemetry.info(
        "request_timing",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(process_time, 2),
        },
    )
    return response


@app.get("/")
async def root():
    return {"message": "Welcome!"}


@app.get("/slow")
async def slow():
    time.sleep(2)
    return {"message": "Simulated slow endpoint for testing logging."}
