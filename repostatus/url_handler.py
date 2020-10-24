"""Handle creation of the URL's"""

from re import match

from simber import Logger


logger = Logger("url_handler")


class URLHandler(object):
    """Handle dynamic creation of URL's for the GitHub API.

    The URL's will be created based on the necessity of the
    request.
    """

    def __init__(self, repo: str) -> None:
        self.repo = self._verify_repo(repo)
        self._BASE_URL = "https://api.github.com/"
        self._type_map = {
            'issue': 'repos/{}/issues',
            'pull': 'repos/{}/pulls?state=all'
        }

    def _verify_repo(self, repo: str) -> str:
        """Verify the format of the passed repo string
        and make sure it is a valid format.

        The allowed format as required by the GitHub API
        is {username}/{reponame}
        """
        if not match(r'^[a-zA-Z0-9\-]*/[a-zA-Z0-9\-]*$', repo):
            logger.critical("Invalid repo passed")
        return repo

    def _build_url(self, type: str) -> str:
        """Build an URL based on the type

        Based on the type passed, build the URL accordingly
        and return the str.
        """
        # Check if type is valid
        if type not in list(self._type_map.keys()):
            logger.critical("Invalid type passed to build")

        return "{}{}".format(
                        self._BASE_URL, self._type_map[type].format(self.repo))

    @property
    def issue_url(self) -> str:
        """Build an issue URL and return it"""
        return self._build_url(type="issue")

    @property
    def pull_url(self) -> str:
        """Build an pull URL and return it"""
        return self._build_url(type="pull")
