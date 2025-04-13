"""create tables table

Revision ID: 0d8217f9116f
Revises:
Create Date: 2025-04-13 17:18:26.829828

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0d8217f9116f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tables",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("seats", sa.Integer(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tables")),
        sa.UniqueConstraint("name", name=op.f("uq_tables_name")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tables")
