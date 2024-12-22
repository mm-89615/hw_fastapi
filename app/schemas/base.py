from typing import Literal

from pydantic import BaseModel


class IdResponseBase(BaseModel):
    id: int


class StatusResponse(BaseModel):
    status: Literal['deleted']


class BaseUserRequest(BaseModel):
    name: str
    password: str
