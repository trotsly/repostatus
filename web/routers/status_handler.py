"""Handle everything related to getting the
status of the repo.
"""

from pydantic import BaseModel, parse_obj_as
from pymongo import MongoClient
from simber import Logger
from fastapi import APIRouter, HTTPException

from config import get_settings
from utils.sessionstate import SessionState
from repostatus.happiness import Happiness


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
    poalrity: float
    emotion: StatusEmotion


class Status(BaseModel):
    issue: StatusEach
    pull: StatusEach
    commit: StatusEach
    total: StatusEach


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
    issue = happiness.issue
    commit = happiness.commit
    pull = happiness.pull
    total = happiness.happiness

    status_object = Status()

    status_object.issue = StatusEach(
        data=StatusData(
            char=issue.chars, word=issue.words, sentence=issue.sentences),
        
    )

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
