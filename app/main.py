"""the main app."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal, engine, metadata
from app.config.logging import configure_logging
from app.exceptions.http import http_exception_handler_logging
from app.routes.ticket import router as ticket_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict[str, Session], None]:
    """Handle application startup and shutdown."""
    # logging
    configure_logging()
    # table creation
    metadata.create_all(engine)
    # db session
    db = SessionLocal()
    yield {"db": db}
    db.close()
    engine.dispose()


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(HTTPException, http_exception_handler_logging)

app.include_router(ticket_router)
