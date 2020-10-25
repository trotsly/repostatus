"""Handle everything related to filtering the data"""

from markdown import markdown
from bs4 import BeautifulSoup
from typing import List


def _markdown_to_text(markdown_str: str) -> str:
    """Parse the markdown string to text and get rid
    of unnecessary things like code chunks, images etc.
    """
    html = markdown(markdown_str)
    text = " ".join(BeautifulSoup(html, "html.parser").findAll(text=True))
    return text


def filter(unfiltered_data: List) -> List:
    """Filter the passed data to get rid of unwanted code
    chunks etc.

    What we will do is parse the markdown to HTML and after
    that parse it back to text using BeautifulSoup
    """
    filtered_data = [_markdown_to_text(unfiltered_str)
                     for unfiltered_str in unfiltered_data]
    return filtered_data
