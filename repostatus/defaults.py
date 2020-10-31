"""Handle all the default values used for
functioning of the app
"""
from os import environ, getenv
from typing import Dict
from base64 import b64encode
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path("~/.cache/repostatus/.env").expanduser())


class Default(object):
    """Store all the default values.

    The values will be exposed to the users
    as a property and they will be otherwise kept
    private
    """
    def __init__(self) -> None:
        self._max_issue_iterate = 15
        self._token = environ.get("GITHUB_TOKEN")
        self.__client_id = getenv("CLIENT_ID")
        self.__client_secret = getenv("CLIENT_SECRET")

    @property
    def max_issue_iterate(self) -> int:
        return self._max_issue_iterate

    @property
    def github_token(self) -> str:
        return self._token

    @property
    def basic_token(self) -> str:
        basic_token = "{}:{}".format(self.__client_id, self.__client_secret)
        basic_token = b64encode(basic_token.encode("ascii"))
        return basic_token.decode("ascii")

    @property
    def token_header(self) -> Dict:
        return {
            "Authorization": "Basic {}".format(self.basic_token)
        }
