"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-10-23
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "caregiver_accounts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "paired_devices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "caregiver_id",
            sa.Integer(),
            sa.ForeignKey("caregiver_accounts.id"),
            nullable=False,
        ),
        sa.Column("device_label", sa.String(length=200), nullable=False),
        sa.Column("token", sa.String(length=64), nullable=False),
        sa.Column("paired_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_paired_devices_token", "paired_devices", ["token"], unique=True)

    op.create_table(
        "encrypted_blobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "device_id",
            sa.Integer(),
            sa.ForeignKey("paired_devices.id"),
            nullable=False,
        ),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("ciphertext", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_encrypted_blobs_category", "encrypted_blobs", ["category"])


def downgrade() -> None:
    op.drop_index("ix_encrypted_blobs_category", table_name="encrypted_blobs")
    op.drop_table("encrypted_blobs")
    op.drop_index("ix_paired_devices_token", table_name="paired_devices")
    op.drop_table("paired_devices")
    op.drop_table("caregiver_accounts")
