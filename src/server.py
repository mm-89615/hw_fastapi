from fastapi import FastAPI

import crud
from constants import STATUS_DELETED
from dependency import SessionDependency
from lifespan import lifespan
from models import Advertisement
from schemes import (GetAdvertisementResponse,
    CreateAdvertisementResponse,
    CreateAdvertisementRequest,
    UpdateAdvertisementResponse,
    DeleteAdvertisementResponse,
    UpdateAdvertisementRequest,
    GetListAdvertisementsResponse)

app = FastAPI(title="Hello World",
    terms_of_service="",
    description="Hello World description",
    lifespan=lifespan)


@app.get(path="/api/v1/advertisement/{ad_id}",
    response_model=GetAdvertisementResponse,
    tags=["advertisement"])
async def get_advertisement(session: SessionDependency, ad_id: int) -> dict[str, int]:
    ad_item = await crud.get_item_by_id(session, Advertisement, ad_id)
    return ad_item.dict


@app.post(path="/api/v1/advertisement",
    response_model=CreateAdvertisementResponse,
    tags=["advertisement"])
async def create_advertisement(session: SessionDependency,
    ad_request: CreateAdvertisementRequest) -> dict[str, int]:
    ad = Advertisement(title=ad_request.title,
        description=ad_request.description,
        price=ad_request.price,
        author=ad_request.author)
    await crud.add_item(session, ad)
    return ad.id_dict


@app.patch(path="/api/v1/advertisement/{ad_id}",
    response_model=UpdateAdvertisementResponse,
    tags=["advertisement"])
async def update_advertisement(session: SessionDependency,
    ad_request: UpdateAdvertisementRequest,
    ad_id: int) -> dict[str, int]:
    ad_json = ad_request.dict(exclude_unset=True)
    ad = await crud.get_item_by_id(session, Advertisement, ad_id)
    for field, value in ad_json.items():
        setattr(ad, field, value)
    await crud.add_item(session, ad)
    return ad.id_dict


@app.delete(path="/api/v1/advertisement/{ad_id}",
    response_model=DeleteAdvertisementResponse,
    tags=["advertisement"])
async def delete_advertisement(session: SessionDependency,
    ad_id: int) -> dict[str, str]:
    ad = await crud.get_item_by_id(session, Advertisement, ad_id)
    await crud.delete_item(session, ad)
    return STATUS_DELETED


@app.get(path="/api/v1/advertisement",
    response_model=GetListAdvertisementsResponse,
    tags=["advertisement"])
async def get_advertisements_by_filters(session: SessionDependency,
    title: str | None = None,
    description: str | None = None,
    price: float | None = None,
    author: str | None = None) -> dict[str, list[GetAdvertisementResponse]]:
    filters = {
        "title": title,
        "description": description,
        "price": price,
        "author": author
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    ads = await crud.get_items_by_filters(session, Advertisement, filters)
    return {"result": [ad.dict for ad in ads]}
