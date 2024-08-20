
from pydantic import BaseModel


class TokenData(BaseModel):
    username: str


class Status(BaseModel):
    message: str
