import datetime
from typing import Sequence

from pydantic import BaseModel

from schemas.base import IdResponseBase, StatusResponse


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str | None
    price: float


class CreateAdvertisementResponse(IdResponseBase):
    pass


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str | None
    price: float
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class GetListAdvertisementsResponse(BaseModel):
    result: Sequence[GetAdvertisementResponse]


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class UpdateAdvertisementResponse(IdResponseBase):
    pass


class DeleteAdvertisementResponse(StatusResponse):
    pass
