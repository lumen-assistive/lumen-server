"""Model pack metadata endpoint.

Serves descriptors only, never model binaries. The catalog starts
empty: no models have been converted, benchmarked, or license-cleared
yet. It is populated once the lumen-models repository produces real
`ModelDescriptor` entries.
"""

from fastapi import APIRouter

from app.schemas import ModelDescriptor

router = APIRouter(prefix="/api/v1/models", tags=["models"])

_SEED_CATALOG: list[ModelDescriptor] = []


@router.get("", response_model=list[ModelDescriptor])
def list_models() -> list[ModelDescriptor]:
    """Returns the current model pack catalog.

    Empty until lumen-models publishes a real, license-cleared catalog.
    """
    return _SEED_CATALOG
