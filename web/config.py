"""Handle the configuration of various variables"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    repostatusdb_uri: str
    client_jwt_secret: str

    class Config:
        env_file = ".env"
