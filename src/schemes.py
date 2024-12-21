import datetime
import uuid
from typing import Literal, Sequence

from pydantic import BaseModel


class IdResponseBase(BaseModel):
    id: int


class StatusResponse(BaseModel):
    status: Literal['deleted']


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str | None
    price: float
    author: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class GetListAdvertisementsResponse(BaseModel):
    result: Sequence[GetAdvertisementResponse]


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str | None
    price: float
    author: str


class CreateAdvertisementResponse(IdResponseBase):
    pass


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None


class UpdateAdvertisementResponse(IdResponseBase):
    pass


class DeleteAdvertisementResponse(StatusResponse):
    pass


class BaseUserRequest(BaseModel):
    name: str
    password: str


class CreateUserRequest(BaseUserRequest):
    pass


class CreateUserResponse(IdResponseBase):
    pass


class LoginRequest(BaseUserRequest):
    pass


class LoginResponse(BaseModel):
    token: uuid.UUID
