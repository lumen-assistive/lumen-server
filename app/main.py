"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import blobs, model_catalog, pairing
from app.db import Base, engine


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Lumen Server",
    description=(
        "Optional, end-to-end encrypted backend for Lumen caregiver sync and model pack metadata."
    ),
    version="0.1.0",
    lifespan=_lifespan,
)

app.include_router(pairing.router)
app.include_router(blobs.router)
app.include_router(model_catalog.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check used by Docker Compose and load balancers."""
    return {"status": "ok"}
