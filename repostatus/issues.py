"""Handle extracting the issues

Extract all the comments from the issues in the
given repo and accordingly return the messages.
"""

from requests import Session, get
from simber import Logger
from repostatus.url_handler import URLHandler, update_header_token
from repostatus import Default

from typing import List


logger = Logger("issue")


def _get_comments_each(comment_url: str, token: str = None) -> List:
    """Get the comments from the passed URL and return a
    list containing those.

    Each issue has some comments excluding the one added when
    the issue was created.
    """
    access_token = Default.token_header if token is None else token
    response = get(comment_url, headers=access_token)
    comments = []

    if response.status_code != 200 or not len(response.json()):
        return comments

    comments = [comment["body"] for comment in response.json()]

    return comments


def get_issue_comments(repo: str, token: str = None) -> List:
    """Get all the comments of the given repo

    Go through all the issues in the passed repo
    and accordingly find all the comments in the
    repo.

    repo: Should be of the form {username}/{reponame}

    where
    username: GitHub username
    reponame: GitHub reponame
    """
    request = URLHandler(repo).issue_request
    comments = []

    if token:
        update_header_token(request, token)

    response = Session().send(request)

    if response.status_code != 200:
        logger.critical("Response was not OK! Message returned: {}".format(
            response.content))

    # Every issues has a body message which will also be a comment
    # and some comments that were added after the base message

    issues_returned = response.json()
    logger.debug("Got {} issues".format(len(issues_returned)))

    issues_returned = issues_returned[:Default.max_issue_iterate]

    for issue in issues_returned:
        first_comment = issue["body"]
        other_comments = _get_comments_each(issue["comments_url"], token)
        comments.append(first_comment)
        comments.extend(other_comments)

    return comments
