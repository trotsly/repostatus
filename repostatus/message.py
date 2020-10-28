"""Handle getting list of repositories and commits and messages.

Fetches a list of repos and commits along with,
its messages

Author:Vedant Baviskar
Date: 27/10/2020
"""

import requests
import json
from repostatus.defaults import Default
from repostatus.url_handler import URLHandler


def get_repo(repo_url) -> list:
    """Fetch the the list of repositories."""
    response = requests.get(repo_url, params=Default.token_header)
    json_data = json.loads(response.content)
    repo_list = json_data
    if response.status_code != 200:
        return []

    return repo_list


"""Now writing a function to get commits from the user repository."""


def get_commit(commit_url) -> dict:
    """Use api to return the commits and the messages."""
    commit = URLHandler(commit_url).commit_request
    response = requests.get(commit, params=Default.token_header)
    json_commit_data = json.loads(response.content)
    for i in json_commit_data:
        print(i)


if __name__ == "__main__":
    """Passing URL to get repo list
    """

    repo_url = input("Enter URL :- ")
    get_repo(repo_url)

    """Passing URL to get commits.
    """

    commit_url = input("Enter URL :- ")
    get_commit(commit_url)
