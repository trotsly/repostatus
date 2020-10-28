"""Handle requests related to repo.

Everything related to the repo like getting
details etc will be handled through this module.
"""

from pydantic import BaseModel
from requests import get
from typing import List, Optional
from fastapi import HTTPException, APIRouter, Header
from requests.api import head

from repostatus import Default

router = APIRouter()


class Repo(BaseModel):
    name: str
    full_name: str
    language: str = None
    stars: int
    url: str


def get_repo_list(username: str, access_token: str) -> List:
    """Get the list of public repos for the username
    passed.

    Use the official GitHub API with the access token
    of the app to access all the public repos of the
    passed user.
    """
    print(access_token)
    REPO_URL = "https://api.github.com/users/{}/repos".format(username)
    response = get(REPO_URL, headers={"Authorization": "token {}".format(
        access_token)})

    if response.status_code != 200:
        raise HTTPException(
                status_code=response.status_code,
                detail=response.reason)

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

    return repos


def extract_access_token(header_content: str) -> str:
    """Extract the token from the passed header string."""
    print(header_content)
    return header_content.split()[1]


@router.get("/{username}", response_model=List[Repo])
def get_repos(username: str, authorization: Optional[str] = Header(None)):
    # Try to extract the access token
    access_token = Default.github_token if authorization is None \
        else extract_access_token(authorization)

    response = get_repo_list(
                    username=username,
                    access_token=access_token)
    return response
