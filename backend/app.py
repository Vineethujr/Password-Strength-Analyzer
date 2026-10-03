from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.db import init_db
from backend.routes.api import router
from backend.utils.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Password Strength Analyzer & Security Suggestion Tool", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.exception_handler(RequestValidationError)
async def safe_validation_error_handler(request: Request, exc: RequestValidationError):
    # Never mirror request bodies or secret values in error responses.
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request. Secret values are not included in validation errors."},
    )

app.include_router(router)
