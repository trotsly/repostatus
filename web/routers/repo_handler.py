"""Handle requests related to repo.

Everything related to the repo like getting
details etc will be handled through this module.
"""

from pydantic import BaseModel
from requests import get
from typing import List, Optional, Dict
from fastapi import HTTPException, APIRouter, Header
from simber import Logger

from repostatus import Default

router = APIRouter()
logger = Logger("repo_handler")


class Repo(BaseModel):
    name: str
    full_name: str
    language: str = None
    stars: int
    url: str


def get_repo_list(username: str, headers: Dict) -> List:
    """Get the list of public repos for the username
    passed.

    Use the official GitHub API with the access token
    of the app to access all the public repos of the
    passed user.
    """
    REPO_URL = "https://api.github.com/users/{}/repos".format(username)

    # Inject a per_page count in the query
    params = {}
    params["per_page"] = 100

    response = get(REPO_URL, headers=headers, params=params)

    if response.status_code != 200:
        logger.info("Response to {} returned with {}:{}".format(
            REPO_URL, response.status_code, response.reason
        ))
        logger.info("passed headers were {}".format(headers))
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
    return header_content.split()[1]


@router.get("/{username}", response_model=List[Repo])
def get_repos(username: str, authorization: Optional[str] = Header(None)):
    # Try to extract the access token
    header = Default.token_header

    if authorization:
        access_token = extract_access_token(authorization)
        header["Authorization"] = "token {}".format(access_token)

    response = get_repo_list(
                    username=username,
                    headers=header)
    return response
