"""We need to handle sessionstate objects by
creating custom class that will be able to
handle the ObjectId that mongo uses.
"""
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class MongoObjectId(ObjectId):
    """This class is derived from ObjectId class
    and overriden in order to add support for
    mongo objects directly through pydantic.

    Following article can be referrenced for more:
    https://medium.com/python-in-plain-english/how-to-use-fastapi-with-mongodb-75b43c8e541d
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_objectid

    @classmethod
    def validate_objectid(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError('Invalid ObjectId passed')
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SessionState(BaseModel):
    id: Optional[MongoObjectId] = Field(alias='_id')
    state: str
    token: str = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
