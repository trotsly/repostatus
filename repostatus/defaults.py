"""Handle all the default values used for
functioning of the app
"""
from os import environ
from typing import Dict


class Default(object):
    """Store all the default values.

    The values will be exposed to the users
    as a property and they will be otherwise kept
    private
    """
    def __init__(self) -> None:
        self._max_issue_iterate = 15
        self._token = environ.get("GITHUB_TOKEN")

    @property
    def max_issue_iterate(self) -> int:
        return self._max_issue_iterate

    @property
    def github_token(self) -> str:
        return self._token

    @property
    def token_header(self) -> Dict:
        return {
            "Authorization": "token {}".format(self._token)
        }
