"""Handle the package as a whole. This should be
the entrypoint for everyone accessing this package
to get the happiness status.
"""
from textblob import TextBlob
from repostatus.filter import filter
from repostatus.issues import get_issue_comments
from repostatus.pulls import get_pull_comments
from repostatus.message import get_commit
from simber import Logger
from typing import List


logger = Logger("happiness")


class HappinessContainer(object):
    """Contain the happiness related data in
    a nice manner so that it's easier to access
    """
    def __init__(self, data: List = [], polarity: float = None) -> None:
        self.__data = data
        self.__polarity = polarity

    @property
    def data(self) -> List:
        return self.__data

    @property
    def polarity(self) -> float:
        return self.__polarity

    @data.setter
    def data(self, value) -> None:
        self.__data = value

    @polarity.setter
    def polarity(self, value) -> None:
        self.__polarity = value

    def __repr__(self) -> str:
        return str(self.__polarity)


class Happiness(object):
    """Handle the happiness related access
    methods.

    This class will be exposed for use to the
    users.
    """
    def __init__(self, repo: str, token: str = None) -> None:
        self.__repo = repo
        self.__token = token
        self.__happiness = {
            "issue": HappinessContainer(),
            "pull": HappinessContainer(),
            "commit": HappinessContainer()
        },
        self.__overall_polarity = None

        # Call all the internal methods
        self._fetch_data()
        self._filter_data()
        self._get_polarity()
        self._calculate_overall_polarity()

    def _fetch_data(self):
        """Fetch the data using various functions from
        different modules.
        """
        logger.info("Fetching content for each")

        self.__happiness["issue"].data = get_issue_comments(self._repo,
                                                            self._token)
        self.__happiness["pull"].data = get_pull_comments(self._repo,
                                                          self._token)
        self.__happiness["commit"].data = get_commit(self._repo, self._token)

    def _filter_data(self):
        """Filter the fetched data and store it in the same
        container"""
        for key in self.__happiness.keys():
            unfiltered_data = self.__happiness[key].data
            self.__happiness[key].data = filter(unfiltered_data)

    def _get_polarity(self):
        """Get the polarity for each of the fethced and cleaned
        data."""
        for key in self.__happiness.keys():
            filtered_data = self.__happiness[key].data
            blob = TextBlob(" ".join(filtered_data))
            self.__happiness[key].polarity = blob.polarity

    def _calculate_overall_polarity(self):
        """Calculate the overall polarity by concatenating all the
        data together and passing it to the blob.
        """
        combined_data_list = [self.__happiness[key].data
                              for key in self.__happiness]
        blob = TextBlob(" ".join(combined_data_list))

        self.__overall_polarity = blob.polarity

    @property
    def issue(self) -> HappinessContainer:
        return self.__happiness["issue"]

    @property
    def pull(self) -> HappinessContainer:
        return self.__happiness["pull"]

    @property
    def commit(self) -> HappinessContainer:
        return self.__happiness["commit"]

    @property
    def polarity(self) -> float:
        return self.__overall_polarity
