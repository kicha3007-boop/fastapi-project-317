"""create url_checks

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-20

"""

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "url_checks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url_id", sa.Integer(), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("h1", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["url_id"], ["urls.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_url_checks_url_id"),
        "url_checks",
        ["url_id"],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_url_checks_url_id"), table_name="url_checks")
    op.drop_table("url_checks")
