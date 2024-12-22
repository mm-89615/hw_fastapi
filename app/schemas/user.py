from pydantic import BaseModel

from schemas.base import IdResponseBase, StatusResponse, BaseUserRequest
from utils.custom_types import Role


class CreateUserRequest(BaseUserRequest):
    pass


class CreateUserResponse(IdResponseBase):
    pass


class GetUserResponse(BaseModel):
    id: int
    name: str
    role: Role


class UpdateUserRequest(BaseUserRequest):
    name: str | None = None
    password: str | None = None
    role: Role | None = None


class UpdateUserResponse(IdResponseBase):
    pass


class DeleteUserResponse(StatusResponse):
    pass
