"""Handle extraction of authorization header"""

from re import sub
from jwt import decode
from jwt.exceptions import DecodeError
from typing import Dict
from os import environ

CLIENT_SECRET = environ.get("CLIENT_SECRET")


def get_bearer(header) -> str:
    """
    Extract the Bearer token from the headers data
    This is especially usefull if more than on Authorization
    headers are passed.
    """
    content = header.split(",")

    for c in content:
        stripped_c = sub(r'^[ ]{1,}', '', c).split()
        if stripped_c[0] == 'Bearer':
            return stripped_c[1]

    return None


def get_jwt_content(jwt_content: str) -> Dict:
    """Extract the content from the JWT and accordingly
    return the content.

    If the token is wrong, then raise DecodeError.
    """

    if jwt_content is None:
        raise DecodeError

    return decode(jwt_content, CLIENT_SECRET)
