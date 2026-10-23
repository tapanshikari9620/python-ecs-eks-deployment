import json
import logging
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

import fastapi
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.config import get_settings


settings = get_settings()


class JsonFormatter(logging.Formatter):
    """Format application logs as JSON for centralized logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())

root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.addHandler(handler)
root_logger.setLevel(
    getattr(logging, settings.log_level, logging.INFO)
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Application starting")
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A Python REST API for AWS deployment practice.",
    lifespan=lifespan,
)


class MessageRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=200,
        description="Message to echo back",
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)

    logger.info(
        "HTTP request processed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
        },
    )
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "details": exc.errors(),
            "path": request.url.path,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": str(exc.detail),
            "path": request.url.path,
        },
        headers=exc.headers,
    )


@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/api/v1/message")
async def get_message():
    return {
        "message": settings.api_message,
        "application": settings.app_name,
    }


@app.get("/api/v1/info")
async def get_info():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "python_version": sys.version.split()[0],
        "fastapi_version": fastapi.__version__,
        "environment": settings.environment,
    }


@app.post("/api/v1/message")
async def create_message(payload: MessageRequest):
    logger.info("Validated message received")

    return {
        "message": payload.message,
        "length": len(payload.message),
        "application": settings.app_name,
    }


def main():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower(),
        access_log=False,
    )


if __name__ == "__main__":
    main()
