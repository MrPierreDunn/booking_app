"""create reservations table

Revision ID: 03842f6e40a7
Revises: 0d8217f9116f
Create Date: 2025-04-14 14:22:35.324363

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "03842f6e40a7"
down_revision: Union[str, None] = "0d8217f9116f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("table_id", sa.Integer(), nullable=False),
        sa.Column("customer_name", sa.String(), nullable=False),
        sa.Column("reservation_time", sa.DateTime(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["table_id"],
            ["tables.id"],
            name=op.f("fk_reservations_table_id_tables"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_reservations")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("reservations")
