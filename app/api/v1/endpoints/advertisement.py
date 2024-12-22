from fastapi import APIRouter, HTTPException

from utils.constants import STATUS_DELETED
from utils.dependency import SessionDependency, TokenDependency
from models import Advertisement
from schemas import (
    GetAdvertisementResponse,
    CreateAdvertisementResponse,
    CreateAdvertisementRequest,
    UpdateAdvertisementResponse,
    UpdateAdvertisementRequest,
    DeleteAdvertisementResponse, GetListAdvertisementsResponse
)
from services import crud

router = APIRouter(tags=["advertisement"], prefix="/api/v1/advertisement")


@router.get(path="/{ad_id}", response_model=GetAdvertisementResponse)
async def get_advertisement(session: SessionDependency, ad_id: int):
    ad_item = await crud.get_item_by_id(session, Advertisement, ad_id)
    return ad_item.dict


@router.post(path="/", response_model=CreateAdvertisementResponse)
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


@router.patch(path="/{ad_id}", response_model=UpdateAdvertisementResponse)
async def update_advertisement(
    session: SessionDependency,
    token: TokenDependency,
    ad_request: UpdateAdvertisementRequest,
    ad_id: int
) -> dict[str, int]:
    ad_json = ad_request.dict(exclude_unset=True)
    ad = await crud.get_item_by_id(session, Advertisement, ad_id)

    if ad.user_id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    for field, value in ad_json.items():
        setattr(ad, field, value)
    await crud.add_item(session, ad)
    return ad.id_dict


@router.delete(path="/{ad_id}", response_model=DeleteAdvertisementResponse)
async def delete_advertisement(
    session: SessionDependency,
    token: TokenDependency,
    ad_id: int
) -> dict[str, str]:
    ad = await crud.get_item_by_id(session, Advertisement, ad_id)
    if ad.user_id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    await crud.delete_item(session, ad)
    return STATUS_DELETED


@router.get(path="/", response_model=GetListAdvertisementsResponse)
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
