"""Handle everything related to getting the
status of the repo.
"""

from pydantic import BaseModel, parse_obj_as
from pymongo import MongoClient
from simber import Logger
from typing import Optional
from fastapi import APIRouter, HTTPException, Header, Query

from config import get_settings
from utils.sessionstate import SessionState
from repostatus.happiness import Happiness
from utils.auth_handler import get_token


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
    emoji: str


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
            emoji=""
        )

        # Update the response
        setattr(status_object, key, StatusEach(
            data=happiness_data,
            polarity=happiness_obj.polarity,
            emotion=happiness_emotion
        ))

    return status_object


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

    # TODO: Handle the below with an exception
    status = Happiness(repo, token)

    response_created = get_parsed_data(status)

    return response_created


@router.get("", response_model=Status)
def calculate_status(authorization: Optional[str] = Header(None),
                     x_state: Optional[str] = Header(None),
                     repo: str = Query(...)) -> Status:
    # If authorization is not None, try to extract the token
    token = get_token(authorization) if authorization is not None else None

    happiness = get_happiness(repo, token, x_state)
    return happiness
