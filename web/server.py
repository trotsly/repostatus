"""Handle the server through various resources"""

from fastapi import FastAPI
from uvicorn import run

from repo_handler import RepoList, get_repo_list
from repostatus import Default

app = FastAPI()


@app.get("/repos/{username}", response_model=RepoList)
async def get_repos(username: str):
    response = get_repo_list(
                    username=username,
                    access_token=Default.github_token)
    return response


if __name__ == "__main__":
    run("server:app", host="0.0.0.0", port=5000, log_level="info")
