"""Handle extraction of authorization header"""

from re import sub


def _get_bearer(header):
    """
    Extract the Bearer token from the headers data
    This is especially usefull if more than on Authorization
    headers are passed.
    """
    content = header.split(",")

    for c in content:
        stripped_c = sub(r'^[ ]{1,}', '', c).split()
        if stripped_c[0] == 'Bearer':
            return stripped_c[1]

    return None
