"""Handle the callback router that will help
with completion of the oauth.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from simber import Logger
from requests import post

from config import get_settings
from assets.html import get_html

logger = Logger("callback_handler", level="DEBUG")
router = APIRouter()

REPOSTATUSDB_URI = get_settings().repostatusdb_uri
client = MongoClient(REPOSTATUSDB_URI)
db = client.repostatus


def is_state_present(state: str) -> bool:
    """Check if the state is present in the database."""
    match = db.sessionstate.find_one({"state": state})
    return True if match else False


def exchange_token(code: str, state: str) -> str:
    """Use the code provided and get the access token.

    Return the access token, once fetched.
    """
    exchange_url = "https://github.com/login/oauth/access_token"
    params = {
        "client_id": get_settings().client_id,
        "client_secret": get_settings().client_secret,
        "code": code
    }
    headers = {
        "accept": "application/json"
    }

    response = post(exchange_url, params=params, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=response.reason)

    return response.json()


def get_access_token(code: str, state: str):
    """We need to use the code provided by GitHub and
    get the access_token.

    We also need to make sure that the state is verified, else
    we will deny the request.
    """
    # Verify that state is present
    if not is_state_present(state):
        raise HTTPException(status_code=403, detail="Invalid state passed")

    # If the state is verified, go ahead and get the access_token
    token_response = exchange_token(code, state)
    token = token_response["access_token"]
    scope = token_response["scope"]

    # Update the database with the token
    db.sessionstate.update_one({"state": state},
                               {"$set": {"token": token, "scope": scope}})

    # Return HTML that will close the window
    return get_html()


@router.get("", response_class=HTMLResponse)
def authenticate(code: str = Query(None), state: str = Query(None)):
    return get_access_token(code, state)
