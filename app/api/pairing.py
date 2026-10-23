"""Device pairing endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import CaregiverAccount, PairedDevice
from app.schemas import PairingRequest, PairingResponse
from app.security import generate_device_token

router = APIRouter(prefix="/api/v1/pairing", tags=["pairing"])


@router.post("", response_model=PairingResponse)
def pair_device(request: PairingRequest, db: Session = Depends(get_db)) -> PairingResponse:
    """Creates a caregiver account and pairs a device to it.

    Each call creates a new caregiver account; the Lumen app is
    expected to call this once per caregiver and reuse the returned
    token for subsequent devices by extending this endpoint, which is
    out of scope for this initial version.
    """
    caregiver = CaregiverAccount(display_name=request.caregiver_display_name)
    db.add(caregiver)
    db.flush()

    device = PairedDevice(
        caregiver_id=caregiver.id,
        device_label=request.device_label,
        token=generate_device_token(),
    )
    db.add(device)
    db.commit()
    db.refresh(device)

    return PairingResponse(device_id=device.id, caregiver_id=caregiver.id, token=device.token)
