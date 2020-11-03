"""Handle the server through various resources"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    repo_handler,
    state_handler,
    callback_handler,
    status_handler,
    badge_handler
)

app = FastAPI(docs_url=None, redoc_url=None)


ORIGINS = [
    "http://localhost:8080",
    "https://repostatus.deepjyoti30.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

app.include_router(
    repo_handler.router,
    prefix="/repos",
    tags=["repos"]
)
app.include_router(
    state_handler.router,
    prefix="/state",
    tags=["state"]
)
app.include_router(
    callback_handler.router,
    prefix="/callback",
    tags=["callback"]
)
app.include_router(
    status_handler.router,
    prefix="/status",
    tags=["status"]
)
app.include_router(
    badge_handler.router,
    prefix="/badge",
    tags=["badge"]
)
