"""Handle HTML responses that will be used
in the handling of the callback.
"""

TYPE_MAP = {
    "success": "assets/success.html",
    "failure": "assets/failure.html"
}


def get_html(type: str = "success") -> str:
    """Return HTML based on the type passed by the
    user.
    """
    file_name = TYPE_MAP.get(type, None)

    if file_name is None:
        return ""

    return str(open(file_name).read())
