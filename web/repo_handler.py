"""Handle requests related to repo.

Everything related to the repo like getting
details etc will be handled through this module.
"""

from pydantic import BaseModel
from requests import get
from typing import List


class Repo(BaseModel):
    name: str
    full_name: str
    language: str = None
    stars: int
    url: str


class RepoList(BaseModel):
    status: str
    results: List[Repo]


def get_repo_list(username: str, access_token: str) -> RepoList:
    """Get the list of public repos for the username
    passed.

    Use the official GitHub API with the access token
    of the app to access all the public repos of the
    passed user.
    """
    REPO_URL = "https://api.github.com/users/{}/repos".format(username)
    response = get(REPO_URL, headers={"Authorization": "token {}".format(
        access_token)})

    if response.status_code != 200:
        return RepoList(
            status=response.reason,
            results=[]
        )

    repos = []
    for repo in response.json():
        repos.append(Repo(
            name=repo["name"],
            full_name=repo["full_name"],
            language=repo["language"],
            stars=repo["stargazers_count"],
            url=repo["html_url"]))

    # Sort on the basis of stars
    repos.sort(reverse=True, key=lambda repo: repo.stars)

    return RepoList(
        status=response.reason,
        results=repos
    )
