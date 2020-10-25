"""Test the pulls module of repostatus"""

from repostatus.pulls import (
    get_pull_comments,
    _get_each_pull_comments
)
from requests import get
from repostatus import Default


def test__get_each_pull_comments():
    """Test the _get_each_pull_comments function

    We will test the function by using a static pull
    URL for the hello-world repo.
    """
    pull_url = "https://api.github.com/repos/octocat/Hello-World/issues/619/comments"

    comments_returned = _get_each_pull_comments(pull_url)

    # Extract the first comment of the issue manually and check
    # if it is the same.
    second_comment = get(
        pull_url,
        headers={"Authorization": "token {}".format(Default.github_token)}
    ).json()[0]["body"]
    second_comment_returned = comments_returned[0]

    assert second_comment == second_comment_returned, \
        "{}:{}, Should be same".format(second_comment, second_comment_returned)


def test_get_pull_comments():
    """Test the get_pull_comments function

    Test the get_pull_comments function by checking the description
    of the first pull request returned.
    """
    repo = "octocat/hello-world"
    url = "https://api.github.com/repos/{}/pulls".format(repo)

    comments_returned = get_pull_comments(repo)

    # Extract the comments manually. We will check if the description
    # of the first pull was extracted properly or not
    first_pull_desc = get(
        url,
        headers={"Authorization": "token {}".format(Default.github_token)}
    ).json()[0]["body"]

    first_pull_desc_ret = comments_returned[0]

    assert first_pull_desc == first_pull_desc_ret, \
        "{}:{}, Should be same!".format(first_pull_desc, first_pull_desc_ret)
