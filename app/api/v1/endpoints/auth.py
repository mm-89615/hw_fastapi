from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from utils.dependency import SessionDependency
from utils.security import check_password
from models import User, Token
from schemas import LoginResponse, LoginRequest
from services import crud

router = APIRouter(tags=["auth"], prefix="/api/v1/login")


@router.post("/", response_model=LoginResponse)
async def login(session: SessionDependency, login_request: LoginRequest):
    user_query = select(User).where(User.name == login_request.name)
    user = await session.scalar(user_query)
    if not user:
        raise HTTPException(status_code=401, detail="User name is incorrect")
    if not check_password(login_request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict
