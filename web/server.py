"""Handle the server through various resources"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from typing import List

from repo_handler import get_repo_list, Repo
from repostatus import Default


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


@app.get("/repos/{username}", response_model=List[Repo])
def get_repos(username: str):
    response = get_repo_list(
                    username=username,
                    access_token=Default.github_token)
    return response


if __name__ == "__main__":
    run("server:app", host="0.0.0.0", port=5000, log_level="info")
