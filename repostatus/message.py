# Importing required libraries
# coding = utf-8

import requests
import json
from os import environ
access_token = environ.get('GITHUB_TOKEN', '935644c71ab107aec12c05943eaa778248a99b6d')


headers = {"Authorization": "token {}".format(access_token)}


def get_repo(username) -> list:
    """Function will fetch the the list of repositories."""

    base_url = "https://api.github.com/users/{username}/repos"
    response = requests.get(base_url, params=headers)
    json_data = json.loads(response.content)
    repo_list = json_data
    if response != 200:
        return []

    return repo_list


"""Now writing a function to get commits from the user repository."""


def get_commit(user_name, repo_name) -> dict:
    """Using api to return the commits and the messages."""

    commit = "https://api.github.com/users/{user_name}/{repo_name}/commits"
    response = requests.get(commit, params=headers)
    json_commit_data = json.loads(response.content)
    for i in json_commit_data:
        print(i)     


if __name__ == "__main__":
    username = input("Enter Username:- ")
    print(get_repo(username)) 

    user_name = input("Enter username:- ")
    repo_name = input("Repository:- ")
    print(get_commit(user_name, repo_name))