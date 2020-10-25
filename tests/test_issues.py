"""Test the issues module with various test cases"""

from repostatus.issues import (
    get_issue_comments,
    _get_comments_each
)
from requests import get
from repostatus import Default


def test__get_comments_each():
    """Test the _get_comments_each function

    The function extracts all the comments on a given repo.
    """
    repo_comments = "https://api.github.com/repos/octocat/Hello-World/issues/647/comments"

    comments_returned = _get_comments_each(repo_comments)

    # Manually extract the comments and check if the numbers are right
    response = get(
        repo_comments,
        headers={"Authorization": "token {}".format(Default.github_token)})
    comments_extracted = []

    comments_extracted = [comment["body"] for comment in response.json()]

    assert comments_extracted == comments_returned, \
        "{}:{}, Should be same".format(comments_extracted, comments_returned)


def test_get_issue_comments():
    """Test the get_issue_comments function

    The function will be tested using the octocat/hello-world
    repo. We will use the function to get the comments and
    manually extract them as well.
    """
    repo = "octocat/hello-world"
    url = "https://api.github.com/repos/{}/issues".format(repo)

    comments_returned = get_issue_comments(repo)

    # Extract the comments manually. We will check if the description
    # of the first issue was extracted properly or not
    first_issue_desc = get(
        url,
        headers={"Authorization": "token {}".format(Default.github_token)}
    ).json()[0]["body"]

    first_issue_desc_ret = comments_returned[0]

    assert first_issue_desc == first_issue_desc_ret, \
        "{}:{}, Should be same!".format(first_issue_desc, first_issue_desc_ret)
