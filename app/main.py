from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import create_tables


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await create_tables()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(api_router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
