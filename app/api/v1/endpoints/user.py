from fastapi import APIRouter, HTTPException

from utils.dependency import SessionDependency, TokenDependency
from utils.security import hash_password
from models import User
from schemas import (
    CreateUserResponse,
    CreateUserRequest,
    GetUserResponse,
    UpdateUserResponse,
    UpdateUserRequest,
    DeleteUserResponse
)
from services import crud

router = APIRouter(tags=["user"], prefix="/api/v1/user")


@router.post("/", response_model=CreateUserResponse)
async def create_user(
    session: SessionDependency,
    user_request: CreateUserRequest
):
    user_request_dict = user_request.dict()
    user_request_dict["password"] = hash_password(user_request_dict["password"])
    user = User(**user_request_dict)
    await crud.add_item(session, user)
    return user.id_dict


@router.get("/{user_id}", response_model=GetUserResponse)
async def get_user(session: SessionDependency, user_id: int):
    user = await crud.get_item_by_id(session, User, user_id)
    return user.dict


@router.patch("/{user_id}", response_model=UpdateUserResponse)
async def update_user(
    session: SessionDependency,
    token: TokenDependency,
    user_request: UpdateUserRequest,
    user_id: int
):
    user_json = user_request.dict(exclude_unset=True)
    user = await crud.get_item_by_id(session, User, user_id)

    if user.id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    for field, value in user_json.items():
        if field == "role" and token.user.role != "admin":
            raise HTTPException(status_code=403, detail="You can't change role")
        setattr(user, field, value)
    await crud.add_item(session, user)
    return user.id_dict


@router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_user(
    session: SessionDependency,
    token: TokenDependency,
    user_id: int
):
    user = await crud.get_item_by_id(session, User, user_id)
    if user.id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    await crud.delete_item(session, user)
    return {"status": "deleted"}
