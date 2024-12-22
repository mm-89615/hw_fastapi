import uuid

from pydantic import BaseModel


class LoginRequest(BaseModel):
    name: str
    password: str


class LoginResponse(BaseModel):
    token: uuid.UUID
