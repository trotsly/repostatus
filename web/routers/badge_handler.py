"""Handle the route related to getting the badge."""

from fastapi import APIRouter, Response, Query
from requests import get

from routers.status_handler import get_happiness


router = APIRouter()


def build_badge(repo: str, style: str = None) -> str:
    """Build the badege request based on the passed repo.

    Fetch the badge content using shields and return
    accordingly.
    """
    emotion_text = "Invalid"
    emotion_color = "grey"
    params = {
        "cacheSeconds": 86400
    }

    try:
        happiness = get_happiness(repo)

        emotion_text = happiness.total.emotion.text
        emotion_color = happiness.total.emotion.color_name
    except Exception:
        pass

    shield_URL = "https://img.shields.io/badge/repostatus-{}-{}".format(
                    emotion_text, emotion_color)

    if style:
        params["style"] = style

    response = get(shield_URL, params=params)

    return response.text


@router.get("")
def get_badge(repo: str = Query(...), style: str = Query(None)):
    """Get the badge for the passed repo and accordingly return
    the badge content.
    """
    badge_content = build_badge(repo, style)

    return Response(content=badge_content,
                    media_type="image/svg+xml;charset=utf-8")
