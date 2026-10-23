"""Pydantic request and response models."""

from datetime import datetime

from pydantic import BaseModel


class PairingRequest(BaseModel):
    """Request to pair a new device to a caregiver account."""

    caregiver_display_name: str
    device_label: str


class PairingResponse(BaseModel):
    """Credentials for a newly paired device.

    `token` is shown exactly once; the app must store it securely and
    present it as a bearer token on every subsequent request.
    """

    device_id: int
    caregiver_id: int
    token: str


class BlobUploadRequest(BaseModel):
    """An encrypted payload a paired device wants to store."""

    category: str
    ciphertext_base64: str


class BlobResponse(BaseModel):
    """A previously stored encrypted payload."""

    id: int
    category: str
    ciphertext_base64: str
    created_at: datetime


class ModelDescriptor(BaseModel):
    """Metadata for one model pack, mirroring lumen_sdk's contract.

    This endpoint serves metadata only; it never serves model binaries.
    The real catalog is populated once the lumen-models repository
    produces converted, benchmarked, license-cleared model packs.
    """

    id: str
    task: str
    quantization: str
    size_bytes: int
    license_id: str
    version: str
