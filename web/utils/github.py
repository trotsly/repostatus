"""Handle internal requests that are to be made in order
to get GitHub related data.
"""

from requests import get


def get_username(token: str) -> str:
    """Use the passed token to get the username
    of the user that gave us access.

    This username is necessary because we will need to
    use it along with the repo to get the details.
    """
    HEADERS = {
        "Authorization": "token {}".format(token)
    }
    usernameURL = "https://api.github.com/user"

    response = get(usernameURL, headers=HEADERS)

    if response.status_code != 200:
        return "Not Found"

    return response.json()["login"]
