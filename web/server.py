"""Handle the server through various resources"""

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    repo_handler,
    state_handler,
    callback_handler,
    status_handler,
    badge_handler
)

# Create parent router
api_router = APIRouter()

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

api_router.include_router(
    repo_handler.router,
    prefix="/repos",
    tags=["repos"]
)
api_router.include_router(
    state_handler.router,
    prefix="/state",
    tags=["state"]
)
api_router.include_router(
    callback_handler.router,
    prefix="/callback",
    tags=["callback"]
)
api_router.include_router(
    status_handler.router,
    prefix="/status",
    tags=["status"]
)
api_router.include_router(
    badge_handler.router,
    prefix="/badge",
    tags=["badge"]
)

app.include_router(api_router, prefix="/repostatus")
