"""Handle the configuration of various variables"""

from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    repostatusdb_uri: str
    client_jwt: str
    client_secret: str
    client_id: str
    redirect_uri: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
