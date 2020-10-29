"""Handle getting list of repositories and commits and messages.

Fetches a list of repos and commits along with,
its messages

Author:Vedant Baviskar
Date: 27/10/2020
"""

from requests import Session
from repostatus.url_handler import URLHandler
from typing import List
from simber import Logger


logger = Logger("commits")


def get_commit(commit_url) -> List:
    """Use api to return the commits and the messages."""
    commits_request = URLHandler(commit_url).commit_request
    commits = []

    # We need to make the same request 5 times in order to
    # get 500 commit messages
    for request_number in range(5):
        commits_request.url += "&page={}".format(request_number + 1)
        response = Session().send(commits_request)

        if response.status_code != 200:
            logger.warning("Failed fetching commits for page: {}".format(
                request_number + 1))
            continue

        response = response.json()
        commits_per_page = [commit["commit"]["message"] for commit in response]

        commits.extend(commits_per_page)

        if len(commits_per_page) < 100:
            # If the commit length was less than 500, seems like
            # no more commits are available.
            break

    return commits
