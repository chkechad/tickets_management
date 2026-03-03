import os
from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.orm import Session

os.environ["ENV_STATE"] = "test"

from app.config.database import Base, SessionLocal, engine, get_db
from app.main import app


@pytest.fixture(scope="function", autouse=True)  # type: ignore[misc]
def setup_db() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()  # type: ignore[misc]
def db() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()  # type: ignore[misc]
def client(db: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = lambda: (yield db)
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()  # type: ignore[misc]
async def aclient(db: Session) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = lambda: (yield db)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1") as aclient:
        yield aclient
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")  # type: ignore[misc]
def anyio_backend() -> str:
    return "asyncio"
