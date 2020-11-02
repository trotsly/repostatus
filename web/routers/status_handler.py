"""Handle everything related to getting the
status of the repo.
"""

from pydantic import BaseModel, parse_obj_as
from pymongo import MongoClient
from simber import Logger
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Header, Query

from config import get_settings
from utils.repostatus import SessionState
from repostatus.happiness import Happiness
from utils.auth_handler import get_token
from utils.github import is_repo_public


logger = Logger("status_handler")
router = APIRouter()

REPOSTATUSDB_URI = get_settings().repostatusdb_uri

client = MongoClient(REPOSTATUSDB_URI)
db = client.repostatus


class StatusData(BaseModel):
    char: int
    word: int
    sentence: int


class StatusEmotion(BaseModel):
    text: str
    color: str
    color_name: str


class StatusEach(BaseModel):
    data: StatusData
    polarity: float
    emotion: StatusEmotion


class Status(BaseModel):
    issue: StatusEach = None
    pull: StatusEach = None
    commit: StatusEach = None
    total: StatusEach = None


def get_token_from_state(state: str) -> str:
    """Get the token from the state provided."""
    session_state = db.sessionstate.find_one({"state": state})

    if session_state is None:
        raise HTTPException(status_code=404, detail="Invalid state passed")

    # Parse the data into SessionState
    session_state = parse_obj_as(SessionState, session_state)

    if session_state.token is None:
        raise HTTPException(status_code=400,
                            detail="OAuth not yet done for the state")

    return session_state.token


def get_parsed_data(happiness: Happiness):
    """Use the passed Hapiness object and create a proper
    returnable data for the response.
    """
    happiness_dict = happiness.to_dict()
    status_object = Status()

    for key in happiness_dict:
        happiness_obj = happiness_dict[key]
        happiness_data = StatusData(
            char=happiness_obj.chars,
            word=happiness_obj.words,
            sentence=happiness_obj.sentences
        )
        happiness_emotion = StatusEmotion(
            text=happiness_obj.emotion,
            color=happiness_obj.color,
            color_name=happiness_obj.color_name
        )

        # Update the response
        setattr(status_object, key, StatusEach(
            data=happiness_data,
            polarity=happiness_obj.polarity,
            emotion=happiness_emotion
        ))

    return status_object


def get_cached_response(repo: str, token: str):
    """Check the database to see if cached response is
    available.
    """
    matched_response = db.cached_responses.find_one({"repo": repo})

    if matched_response is None:
        return None

    if matched_response["is_public"]:
        return matched_response["response"]

    # If the repo is not private, we need to make sure the token is
    # same
    if matched_response["token"] == token:
        return matched_response["response"]

    return None


def store_cached_response(repo: str, token: str, response: Status):
    """Store the repo response in the database."""
    is_public = is_repo_public(repo)
    response_dict = response.dict(by_alias=True)

    db.cached_responses.insert_one({
        "repo": repo,
        "is_public": is_public,
        "response": response_dict,
        "token": token,
        "date": datetime.utcnow()
    })


def get_happiness(repo: str, token: str = None, state: str = None) -> Status:
    """Calculate the happiness of the passed repo.

    We need to access the repo. Token will be found in the following
    order:

    If state is provided, we will ignore the token
    Else If token is provided, we will use that.
    Else we will use the default token of the app.
    """
    if state:
        token = get_token_from_state(state)

    # Check if cached response is available
    cached_response = get_cached_response(repo, token)

    if cached_response is not None:
        return parse_obj_as(Status, cached_response)

    try:
        status = Happiness(repo, token)
    except Exception:
        raise HTTPException(status_code=404,
                            detail="Repo not found or inaccessible")

    response_created = get_parsed_data(status)

    # Cache the response
    store_cached_response(repo, token, response_created)

    return response_created


@router.get("", response_model=Status)
def calculate_status(authorization: Optional[str] = Header(None),
                     x_state: Optional[str] = Header(None),
                     repo: str = Query(...)) -> Status:
    # If authorization is not None, try to extract the token
    token = get_token(authorization) if authorization is not None else None

    happiness = get_happiness(repo, token, x_state)
    return happiness
