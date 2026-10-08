from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401
from app.core.database import Base, get_session
from app.core.security import hash_password
from app.main import app
from app.models import User


@pytest.fixture
async def session_factory() -> AsyncIterator[async_sessionmaker]:
    engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


@pytest.fixture
async def client(session_factory) -> AsyncIterator[AsyncClient]:
    async def override() -> AsyncIterator:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


async def _login(client: AsyncClient, email: str, password: str) -> dict[str, str]:
    r = await client.post("/api/v1/auth/login", data={"username": email, "password": password})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture
async def user_headers(client) -> dict[str, str]:
    await client.post("/api/v1/auth/register", json={"email": "u@example.com", "password": "password123"})
    return await _login(client, "u@example.com", "password123")


@pytest.fixture
async def admin_headers(client, session_factory) -> dict[str, str]:
    async with session_factory() as s:
        s.add(User(email="a@example.com", hashed_password=hash_password("password123"), is_admin=True))
        await s.commit()
    return await _login(client, "a@example.com", "password123")
