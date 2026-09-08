"""add verification registry tables

Revision ID: b46e5f81425c
Revises: 4695565019df
Create Date: 2026-09-08 20:01:31.328536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b46e5f81425c'
down_revision: Union[str, Sequence[str], None] = '4695565019df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create verification registry tables."""

    op.create_table(
        "registry_blacklist",
        sa.Column("pan_number", sa.String(length=10), nullable=False),
        sa.Column("gstin", sa.String(length=15), nullable=True),
        sa.Column("entity_name", sa.String(length=255), nullable=False),
        sa.Column("blacklisted", sa.Boolean(), nullable=True),
        sa.Column("reason", sa.String(), nullable=True),
        sa.Column("valid_until", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("pan_number"),
    )
    op.create_index(
        "ix_registry_blacklist_pan_number",
        "registry_blacklist",
        ["pan_number"],
        unique=False,
    )
    op.create_index(
        "ix_registry_blacklist_gstin",
        "registry_blacklist",
        ["gstin"],
        unique=False,
    )

    op.create_table(
        "registry_gst",
        sa.Column("gstin", sa.String(length=15), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("trade_name", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("registration_date", sa.String(length=20), nullable=True),
        sa.Column("business_type", sa.String(length=100), nullable=True),
        sa.Column("return_filing_status", sa.String(length=50), nullable=True),
        sa.Column("principal_place_of_business", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("gstin"),
    )
    op.create_index(
        "ix_registry_gst_gstin",
        "registry_gst",
        ["gstin"],
        unique=False,
    )

    op.create_table(
        "registry_pan",
        sa.Column("pan_number", sa.String(length=10), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("pan_number"),
    )
    op.create_index(
        "ix_registry_pan_pan_number",
        "registry_pan",
        ["pan_number"],
        unique=False,
    )

    op.create_table(
        "registry_udyam",
        sa.Column("udyam_number", sa.String(length=30), nullable=False),
        sa.Column("enterprise_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("classification", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("udyam_number"),
    )
    op.create_index(
        "ix_registry_udyam_udyam_number",
        "registry_udyam",
        ["udyam_number"],
        unique=False,
    )

    op.create_table(
        "registry_epfo",
        sa.Column("establishment_id", sa.String(length=50), nullable=False),
        sa.Column("establishment_name", sa.String(length=255), nullable=False),
        sa.Column("contribution_status", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("last_compliant_period", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("establishment_id"),
    )
    op.create_index(
        "ix_registry_epfo_establishment_id",
        "registry_epfo",
        ["establishment_id"],
        unique=False,
    )

    op.create_table(
        "registry_esic",
        sa.Column("employer_code", sa.String(length=50), nullable=False),
        sa.Column("establishment_name", sa.String(length=255), nullable=False),
        sa.Column("employer_name", sa.String(length=255), nullable=True),
        sa.Column("registration_date", sa.String(length=20), nullable=True),
        sa.Column("registration_status", sa.String(length=50), nullable=False),
        sa.Column("contribution_status", sa.String(length=50), nullable=False),
        sa.Column("last_compliant_period", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("employer_code"),
    )
    op.create_index(
        "ix_registry_esic_employer_code",
        "registry_esic",
        ["employer_code"],
        unique=False,
    )

    op.create_table(
        "registry_income_tax",
        sa.Column("pan_number", sa.String(length=10), nullable=False),
        sa.Column("taxpayer_name", sa.String(length=255), nullable=False),
        sa.Column("assessment_year", sa.String(length=20), nullable=False),
        sa.Column("filing_status", sa.String(length=50), nullable=False),
        sa.Column("return_filing_date", sa.String(length=20), nullable=True),
        sa.Column("gross_total_income", sa.String(length=50), nullable=True),
        sa.Column("taxable_income", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("pan_number"),
    )
    op.create_index(
        "ix_registry_income_tax_pan_number",
        "registry_income_tax",
        ["pan_number"],
        unique=False,
    )

    op.create_table(
        "registry_startup_india",
        sa.Column("certificate_number", sa.String(length=50), nullable=False),
        sa.Column("startup_name", sa.String(length=255), nullable=False),
        sa.Column("recognition_date", sa.String(length=20), nullable=True),
        sa.Column("entity_type", sa.String(length=100), nullable=True),
        sa.Column("pan_number", sa.String(length=10), nullable=False),
        sa.Column("validity_status", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("certificate_number"),
    )
    op.create_index(
        "ix_registry_startup_india_certificate_number",
        "registry_startup_india",
        ["certificate_number"],
        unique=False,
    )
    op.create_index(
        "ix_registry_startup_india_pan_number",
        "registry_startup_india",
        ["pan_number"],
        unique=False,
    )


def downgrade() -> None:
    """Drop verification registry tables."""

    op.drop_index(
        "ix_registry_startup_india_pan_number",
        table_name="registry_startup_india",
    )
    op.drop_index(
        "ix_registry_startup_india_certificate_number",
        table_name="registry_startup_india",
    )
    op.drop_table("registry_startup_india")

    op.drop_index(
        "ix_registry_income_tax_pan_number",
        table_name="registry_income_tax",
    )
    op.drop_table("registry_income_tax")

    op.drop_index(
        "ix_registry_esic_employer_code",
        table_name="registry_esic",
    )
    op.drop_table("registry_esic")

    op.drop_index(
        "ix_registry_epfo_establishment_id",
        table_name="registry_epfo",
    )
    op.drop_table("registry_epfo")

    op.drop_index(
        "ix_registry_udyam_udyam_number",
        table_name="registry_udyam",
    )
    op.drop_table("registry_udyam")

    op.drop_index(
        "ix_registry_pan_pan_number",
        table_name="registry_pan",
    )
    op.drop_table("registry_pan")

    op.drop_index(
        "ix_registry_gst_gstin",
        table_name="registry_gst",
    )
    op.drop_table("registry_gst")

    op.drop_index(
        "ix_registry_blacklist_gstin",
        table_name="registry_blacklist",
    )
    op.drop_index(
        "ix_registry_blacklist_pan_number",
        table_name="registry_blacklist",
    )
    op.drop_table("registry_blacklist")
