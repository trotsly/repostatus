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
from requests import Session
from typing import List, Dict

from repostatus.url_handler import URLHandler, update_header_token


logger = Logger("happiness")


class HappinessContainer(object):
    """Contain the happiness related data in
    a nice manner so that it's easier to access
    """
    def __init__(self, data: List = [], polarity: float = None) -> None:
        self.__data = data
        self.__polarity = polarity
        self.__emotion = self.__map_emotions(polarity)
        self.__data_compiled = None
        self.__color_emotion_map = {
            "angry": {
                "hex": "#F44336",
                "name": "red"
            },
            "sad": {
                "hex": "#E29578",
                "name": "orange"
            },
            "happy": {
                "hex": "#83C5BE",
                "name": "green"
            },
            "balanced": {
                "hex": "#006D77",
                "name": "blue"
            }
        }

    @property
    def data(self) -> List:
        return self.__data

    @property
    def words(self) -> int:
        return len(self.data_compiled.split(" "))

    @property
    def chars(self) -> int:
        return len(self.data_compiled)

    @property
    def sentences(self) -> int:
        return len(self.data_compiled.split("\n"))

    @property
    def data_compiled(self) -> str:
        if not self.__data_compiled:
            self.__data_compiled = " ".join(self.data)
        return self.__data_compiled

    @property
    def polarity(self) -> float:
        return self.__polarity

    @property
    def emotion(self) -> str:
        return self.__emotion

    @property
    def color(self) -> str:
        return self.__color_emotion_map.get(self.__emotion, "").get("hex", "")

    @property
    def color_name(self) -> str:
        return self.__color_emotion_map.get(self.__emotion, "").get("name", "")

    @data.setter
    def data(self, value) -> None:
        self.__data = value

    @polarity.setter
    def polarity(self, value) -> None:
        self.__polarity = value
        self.__emotion = self.__map_emotions(value)

    @emotion.setter
    def emotion(self, value: str) -> None:
        self.__emotion = value

    def __repr__(self) -> str:
        return "polarity: {}, emotion: {}".format(
                                self.__polarity, self.__emotion)

    def __map_emotions(self, polarity: float) -> str:
        """Once the polarity calculations are done, we need to
        map the numbers to a word that will make it easier for
        users to understand.
        """
        if polarity is None:
            return ""

        if polarity < -0.5:
            return "angry"
        elif polarity < 0:
            return "sad"
        elif polarity < 0.2:
            return "balanced"
        else:
            return "happy"


class Happiness(object):
    """Handle the happiness related access
    methods.

    This class will be exposed for use to the
    users.
    """
    def __init__(
            self,
            repo: str,
            token: str = None,
            log_level: str = None
    ) -> None:
        self.__repo = repo
        self.__token = token
        self.__happiness = {
            "issue": HappinessContainer(),
            "pull": HappinessContainer(),
            "commit": HappinessContainer()
        }
        self.__overall_polarity = HappinessContainer()

        # Call all the internal methods
        self.__update_log_level(log_level)
        self.__fetch_data()
        self.__filter_data()
        self.__get_polarity()
        self.__calculate_overall_polarity()

    def __repo_exists(self) -> bool:
        """Check if the repo exists or not. If it does not
        exist, raise an exception stating that it does not
        exist or is inaccessible"""
        check_request = URLHandler(self.__repo).check_request

        if self.__token:
            update_header_token(check_request, self.__token)

        logger.debug(check_request.headers)

        response = Session().send(check_request)

        return True if response.status_code == 200 else False

    def __fetch_data(self):
        """Fetch the data using various functions from
        different modules.
        """
        # Raise exception if repo does not exist
        if not self.__repo_exists():
            raise Exception("Repo does not exist")

        logger.debug("Fetching content for each")

        self.__happiness["issue"].data = get_issue_comments(self.__repo,
                                                            self.__token)
        self.__happiness["pull"].data = get_pull_comments(self.__repo,
                                                          self.__token)
        self.__happiness["commit"].data = get_commit(self.__repo, self.__token)

    def __filter_data(self):
        """Filter the fetched data and store it in the same
        container"""
        logger.debug("Filtering the data")

        for key in self.__happiness.keys():
            unfiltered_data = self.__happiness[key].data
            self.__happiness[key].data = filter(unfiltered_data)

    def __get_polarity(self):
        """Get the polarity for each of the fethced and cleaned
        data."""
        logger.debug("Getting the polarity for each")

        for key in self.__happiness.keys():
            filtered_data = self.__happiness[key].data
            blob = TextBlob(" ".join(filtered_data))
            self.__happiness[key].polarity = blob.polarity

    def __calculate_overall_polarity(self):
        """Calculate the overall polarity by concatenating all the
        data together and passing it to the blob.
        """
        logger.debug("Calculating overall polarity")

        combined_data_list = []
        for key in self.__happiness:
            combined_data_list.extend(self.__happiness[key].data)

        blob = TextBlob(" ".join(combined_data_list))

        self.__overall_polarity.data = combined_data_list
        self.__overall_polarity.polarity = blob.polarity

    def __update_log_level(self, level: str) -> None:
        """Update the log level of the logger based on user
        input.
        """
        if level is None:
            return

        logger.update_level(level)

    def to_dict(self) -> Dict:
        """Return a dictionary of all the properties"""
        return {
            "issue": self.issue,
            "pull": self.pull,
            "commit": self.commit,
            "total": self.happiness
        }

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
    def happiness(self) -> HappinessContainer:
        return self.__overall_polarity
