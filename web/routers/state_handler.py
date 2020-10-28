"""Handle everything related to the state endpoint

The state route will support two methods, both of
which will have specific works
"""

from uuid import uuid4
from pymongo import MongoClient
from os import environ


REPOSTATUSDB_URI = environ.get("REPOSTATUSDB_URI")


# Create a client to access mongodb
client = MongoClient(REPOSTATUSDB_URI)
db = client.repostatus
