from fastapi import FastAPI

from api.v1 import user, advertisement, auth
from utils.lifespan import lifespan

app = FastAPI(
    title="Hello World",
    terms_of_service="",
    description="Hello World description",
    lifespan=lifespan
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(advertisement.router)
