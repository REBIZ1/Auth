"""add default role_id

Revision ID: e1cab41f25ab
Revises: 370823d4da65
Create Date: 2026-06-17 20:41:44.481349

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = "e1cab41f25ab"
down_revision: Union[str, Sequence[str], None] = "370823d4da65"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users",
        "role_id",
        existing_type=sa.Integer(),
        nullable=False,
        server_default=text("1"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users",
        "role_id",
        existing_type=sa.Integer(),
        nullable=True,
        server_default=None,
    )
