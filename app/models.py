"""SQLAlchemy ORM models.

The server never stores plaintext caregiver or sensor data: calendar
entries, daily status, and similar records are encrypted on-device by
the Lumen app before upload and stored here as opaque blobs the server
cannot decrypt. See `EncryptedBlob`.
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class CaregiverAccount(Base):
    """A caregiver who can pair devices and receive consented alerts."""

    __tablename__ = "caregiver_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    devices: Mapped[list["PairedDevice"]] = relationship(back_populates="caregiver")


class PairedDevice(Base):
    """A device paired to a caregiver account, authenticated by a token.

    The token is generated once at pairing time and stored as-is; it
    functions as a long-lived API key scoped to this device, not as a
    password, so it is not hashed.
    """

    __tablename__ = "paired_devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    caregiver_id: Mapped[int] = mapped_column(ForeignKey("caregiver_accounts.id"))
    device_label: Mapped[str] = mapped_column(String(200))
    token: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    paired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    caregiver: Mapped[CaregiverAccount] = relationship(back_populates="devices")
    blobs: Mapped[list["EncryptedBlob"]] = relationship(back_populates="device")


class EncryptedBlob(Base):
    """An opaque, client-encrypted payload uploaded by a paired device.

    `category` lets a device fetch its own blobs by kind (for example
    `daily-status` or `calendar`) without the server knowing their
    content. `ciphertext` is stored exactly as uploaded; the server has
    no decryption key.
    """

    __tablename__ = "encrypted_blobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("paired_devices.id"))
    category: Mapped[str] = mapped_column(String(100), index=True)
    ciphertext: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    device: Mapped[PairedDevice] = relationship(back_populates="blobs")
