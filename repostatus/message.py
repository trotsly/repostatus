"""Handle getting list of repositories and commits and messages.

Fetches a list of repos and commits along with,
its messages

Author:Vedant Baviskar
Date: 27/10/2020
"""

import requests
import json
import os

client_token = os.environ.get('access_token')

headers = {"Authorization": "token {}".format(client_token)}


def get_repo(username) -> list:
    """Fetch the the list of repositories."""
    base_url = "https://api.github.com/users/{username}/repos"
    response = requests.get(base_url, params=headers)
    json_data = json.loads(response.content)
    repo_list = json_data
    if response != 200:
        return []

    return repo_list


"""Now writing a function to get commits from the user repository."""


def get_commit(user_name, repo_name) -> dict:
    """Use api to return the commits and the messages."""
    commit = "https://api.github.com/repos/{user_name}/{repo_name}/commits"
    response = requests.get(commit, params=headers)
    json_commit_data = json.loads(response.content)
    for i in json_commit_data:
        print(i)


if __name__ == "__main__":
    """Passing username
    """

    username = input("Enter Username:- ")
    print(get_repo(username))

    """Passing repo name and commit messages"""

    user_name = input("Enter username:- ")
    repo_name = input("Repository:- ")
    print(get_commit(user_name, repo_name))