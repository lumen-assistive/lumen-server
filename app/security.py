"""Device pairing token generation and verification."""

import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import PairedDevice

_bearer_scheme = HTTPBearer()


def generate_device_token() -> str:
    """Generates a new, unguessable device pairing token."""
    return secrets.token_urlsafe(32)


def get_current_device(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> PairedDevice:
    """Resolves the paired device identified by the bearer token.

    Raises a 401 if no device matches the presented token.
    """
    device = db.query(PairedDevice).filter_by(token=credentials.credentials).first()
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unknown or revoked device token.",
        )
    return device
