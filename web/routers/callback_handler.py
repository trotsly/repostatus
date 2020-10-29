"""Handle the callback router that will help
with completion of the oauth.
"""

from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from simber import Logger
from requests import post

from config import get_settings

logger = Logger("callback_handler")
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
        "code": code,
        "redirect_uri": get_settings().redirect_uri,
        "state": state
    }
    headers = {
        "accept": "application/json"
    }

    response = post(exchange_url, params=params, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=response.reason)

    return response.json()["access_token"]


def generate_html() -> str:
    """Generate the HTML that will close the users window with a
    message.
    """
    pass


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
    access_token = get_access_token(code, state)

    # Update the database with the token
    db.sessionstate.update_one({"state": state},
                               {"$set": {"token": access_token}})

    # Return HTML that will close the window
    return generate_html()
