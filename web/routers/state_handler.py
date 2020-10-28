"""Handle everything related to the state endpoint

The state route will support two methods, both of
which will have specific works
"""

from uuid import uuid4
from pymongo import MongoClient
from os import environ
from simber import Logger
from pydantic import BaseModel
from fastapi import APIRouter
from typing import List

from utils.sessionstate import SessionState
from utils.github import get_username
from routers.repo_handler import Repo


logger = Logger("state_handler")
router = APIRouter()

REPOSTATUSDB_URI = environ.get("REPOSTATUSDB_URI")

client = MongoClient(REPOSTATUSDB_URI)
db = client.repostatus


class State(BaseModel):
    state: str


class UserRepo(BaseModel):
    state: str
    username: str
    repo: List[Repo] = []


def create_state() -> str:
    """Create a session state that will be unique.

    Once the state is created, store it in the database
    and return it to the user.
    """
    unique_state = str(uuid4())
    session_state = SessionState(
        state=unique_state
    )

    if hasattr(session_state, "id"):
        delattr(session_state, "id")

    db.sessionstate.insert_one(session_state.dict(by_alias=True))

    return State(state=unique_state)


def get_user_and_repo(jwt_content) -> UserRepo:
    """Extract the content from the jwt passed and accordingly
    find the username and repo of the user and return.

    if the token is wrong, raise an exception.
    """


@router.get("/", response_model=State)
def get_state():
    state = create_state()
    return state
