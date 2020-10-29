"""Handle the server through various resources"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from routers import repo_handler, state_handler, callback_handler

app = FastAPI()


ORIGINS = [
    "http://localhost:8080"
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
    tags=["routers"]
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


if __name__ == "__main__":
    run("server:app", host="0.0.0.0", port=5000, log_level="info")
