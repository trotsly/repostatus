"""Handle creation of the URL's"""

from re import match
from simber import Logger
from requests.models import PreparedRequest
from requests import Request


logger = Logger("url_handler")


class URLHandler(object):
    """Handle dynamic creation of URL's for the GitHub API.

    The URL's will be created based on the necessity of the
    request.
    """

    def __init__(self, repo: str) -> None:
        self.repo = self._verify_repo(repo)
        self._BASE_URL = "https://api.github.com/"
        self._HEADERS = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'repostatus'
        }
        self._type_map = {
            'issue': {
                'url': 'repos/{}/issues',
                'params': {}
            },
            'pull': {
                'url': 'repos/{}/pulls',
                'params': {
                    'state': 'all'
                }
            }
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

    def _build_request(self, type: str) -> PreparedRequest:
        """Build a request based on the passed type
        and add necessary parameters and headers.
        """
        type_data = self._type_map.get(type, None)
        if type_data is None:
            logger.critical("Invalid url type passed")

        request_url = "{}{}".format(
                                self._BASE_URL,
                                type_data["url"].format(self.repo))
        request_params = type_data["params"]

        prepared_request = Request(
                            "GET",
                            request_url,
                            params=request_params,
                            headers=self._HEADERS).prepare()
        return prepared_request

    @property
    def issue_request(self) -> PreparedRequest:
        """Build an issue URL and return it"""
        return self._build_request(type="issue")

    @property
    def pull_request(self) -> PreparedRequest:
        """Build an pull URL and return it"""
        return self._build_request(type="pull")
