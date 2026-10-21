"""create urls

Revision ID: 0001
Revises:
Create Date: 2026-10-20

"""

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "urls",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_urls_name"), "urls", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_urls_name"), table_name="urls")
    op.drop_table("urls")
