from fastapi import FastAPI, HTTPException
from sqlalchemy import select

import crud
from auth import hash_password, check_password
from constants import STATUS_DELETED
from dependency import SessionDependency, TokenDependency
from lifespan import lifespan
from models import Advertisement, User, Token
from schemes import (
    GetAdvertisementResponse,
    CreateAdvertisementResponse,
    CreateAdvertisementRequest,
    UpdateAdvertisementResponse,
    DeleteAdvertisementResponse,
    UpdateAdvertisementRequest,
    GetListAdvertisementsResponse,
    CreateUserResponse,
    CreateUserRequest,
    LoginRequest,
    LoginResponse
)

app = FastAPI(
    title="Hello World",
    terms_of_service="",
    description="Hello World description",
    lifespan=lifespan
)


@app.get(
    path="/api/v1/advertisement/{ad_id}",
    response_model=GetAdvertisementResponse,
    tags=["advertisement"]
)
async def get_advertisement(session: SessionDependency, ad_id: int) -> dict[str, int]:
    ad_item = await crud.get_item_by_id(session, Advertisement, ad_id)
    return ad_item.dict


@app.post(
    path="/api/v1/advertisement",
    response_model=CreateAdvertisementResponse,
    tags=["advertisement"]
)
async def create_advertisement(
    session: SessionDependency,
    token: TokenDependency,
    ad_request: CreateAdvertisementRequest
) -> dict[str, int]:
    ad = Advertisement(
        title=ad_request.title,
        description=ad_request.description,
        price=ad_request.price,
        user_id=token.user_id
    )
    await crud.add_item(session, ad)
    return ad.id_dict


@app.patch(
    path="/api/v1/advertisement/{ad_id}",
    response_model=UpdateAdvertisementResponse,
    tags=["advertisement"]
)
async def update_advertisement(
    session: SessionDependency,
    token: TokenDependency,
    ad_request: UpdateAdvertisementRequest,
    ad_id: int
) -> dict[str, int]:
    ad_json = ad_request.dict(exclude_unset=True)
    ad = await crud.get_item_by_id(session, Advertisement, ad_id)

    if ad.user_id != token.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    for field, value in ad_json.items():
        setattr(ad, field, value)
    await crud.add_item(session, ad)
    return ad.id_dict


@app.delete(
    path="/api/v1/advertisement/{ad_id}",
    response_model=DeleteAdvertisementResponse,
    tags=["advertisement"]
)
async def delete_advertisement(
    session: SessionDependency,
    token: TokenDependency,
    ad_id: int
) -> dict[str, str]:
    ad = await crud.get_item_by_id(session, Advertisement, ad_id)
    if ad.user_id != token.user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    await crud.delete_item(session, ad)
    return STATUS_DELETED


@app.get(
    path="/api/v1/advertisement",
    response_model=GetListAdvertisementsResponse,
    tags=["advertisement"]
)
async def get_advertisements_by_filters(
    session: SessionDependency,
    title: str | None = None,
    description: str | None = None,
    price: float | None = None,
    user_id: int | None = None
) -> dict[str, list[GetAdvertisementResponse]]:
    filters = {
        "title": title,
        "description": description,
        "price": price,
        "user_id": user_id
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    ads = await crud.get_items_by_filters(session, Advertisement, filters)
    return {"result": [ad.dict for ad in ads]}


@app.post(path="/api/v1/user", response_model=CreateUserResponse, tags=["user"])
async def create_user(
    session: SessionDependency,
    user_request: CreateUserRequest
) -> dict[str, int]:
    user_request_dict = user_request.dict()
    user_request_dict["password"] = hash_password(user_request_dict["password"])
    user = User(**user_request_dict)
    await crud.add_item(session, user)
    return user.id_dict


@app.post(path="/api/v1/login", response_model=LoginResponse, tags=["user"])
async def login(
    session: SessionDependency,
    login_request: LoginRequest
) -> dict[str, str]:
    user_query = select(User).where(User.name == login_request.name)
    user = await session.scalar(user_query)
    if not user:
        raise HTTPException(status_code=401, detail="User name is incorrect")
    if not check_password(login_request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict
