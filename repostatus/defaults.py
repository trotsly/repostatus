"""Handle all the default values used for
functioning of the app
"""


class Default(object):
    """Store all the default values.

    The values will be exposed to the users
    as a property and they will be otherwise kept
    private
    """
    def __init__(self) -> None:
        self._max_issue_iterate = 15

    @property
    def max_issue_iterate(self) -> int:
        return self._max_issue_iterate
