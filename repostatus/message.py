"""Handle getting list of repositories and commits and messages.

Fetches a list of repos and commits along with,
its messages

Author:Vedant Baviskar
Date: 27/10/2020
"""

import requests
from repostatus.url_handler import URLHandler


"""Defining a function to get commits from the user repository."""


def get_commit(commit_url) -> dict:
    """Use api to return the commits and the messages."""
    commits = URLHandler(commit_url).commit_request
    response = requests.session().send(commits)

    if response.status_code != 200:
        print("Something went wrong")

    fetched_commits = response.json()
    for commit in fetched_commits:
        return commit


if __name__ == "__main__":
    """Passing URL to get commits.
    """

    commit_url = input("Enter URL :- ")
    get_commit(commit_url)
