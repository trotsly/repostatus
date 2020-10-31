"""Handle extracting the pulls

Extract the comments and all kinds of conversation
from the pull requests and accordingly return
those.
"""

from requests import Session, get
from simber import Logger
from repostatus.url_handler import URLHandler, update_header_token
from repostatus import Default

from typing import List, Dict


logger = Logger("pulls")


def _get_each_pull_comments(pull_url: str, token: Dict = None) -> List:
    """Get the comments of each pull

    Make a request to the given url and accordingly
    extract the comments of the given PR
    """
    access_token = Default.token_header if token is None else token
    response = get(pull_url, headers=access_token)
    comments = []

    if response.status_code != 200 or not len(response.json()):
        return comments

    for comment in response.json():
        comments.append(comment["body"])

    return comments


def get_pull_comments(repo: str, token: str = None) -> List:
    """Get the comments from the pull requests in
    the passed repo.

    Go through all the pull requests and accordingly
    find all the comments and return a list of those
    in the given repo.

    repo: Should be of the form {username}/{reponame}

    where
    username: GitHub username
    reponame: GitHub reponame
    """
    request = URLHandler(repo).pull_request
    comments = []

    if token:
        update_header_token(request, token)

    response = Session().send(request)

    if response.status_code != 200:
        logger.critical("Response was not OK! Message returned: {}".format(
            response.content))

    # The pulls can have a body as well as other comments.
    # We will have to extract all of those into the list

    pulls_returned = response.json()
    logger.debug("Got {} pulls".format(len(pulls_returned)))

    for pull in response.json():
        pull_body = pull["body"]
        other_comments = _get_each_pull_comments(pull["comments_url"],
                                                 request.headers)
        comments.append(pull_body)
        comments.extend(other_comments)

    return comments
