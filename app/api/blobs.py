"""Encrypted blob upload and retrieval.

The server stores and returns ciphertext exactly as provided by the
client; it never has the key needed to decrypt it.
"""

import base64
import binascii

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import EncryptedBlob, PairedDevice
from app.schemas import BlobResponse, BlobUploadRequest
from app.security import get_current_device

router = APIRouter(prefix="/api/v1/blobs", tags=["blobs"])


def _to_response(blob: EncryptedBlob) -> BlobResponse:
    return BlobResponse(
        id=blob.id,
        category=blob.category,
        ciphertext_base64=base64.b64encode(blob.ciphertext).decode("ascii"),
        created_at=blob.created_at,
    )


@router.post("", response_model=BlobResponse)
def upload_blob(
    request: BlobUploadRequest,
    device: PairedDevice = Depends(get_current_device),
    db: Session = Depends(get_db),
) -> BlobResponse:
    """Stores an encrypted payload uploaded by the authenticated device."""
    try:
        ciphertext = base64.b64decode(request.ciphertext_base64, validate=True)
    except binascii.Error as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ciphertext_base64 is not valid base64.",
        ) from error

    blob = EncryptedBlob(device_id=device.id, category=request.category, ciphertext=ciphertext)
    db.add(blob)
    db.commit()
    db.refresh(blob)

    return _to_response(blob)


@router.get("", response_model=list[BlobResponse])
def list_blobs(
    category: str | None = None,
    device: PairedDevice = Depends(get_current_device),
    db: Session = Depends(get_db),
) -> list[BlobResponse]:
    """Lists the authenticated device's own blobs, optionally filtered."""
    query = db.query(EncryptedBlob).filter_by(device_id=device.id)
    if category is not None:
        query = query.filter_by(category=category)
    blobs = query.order_by(EncryptedBlob.created_at.desc()).all()
    return [_to_response(blob) for blob in blobs]
