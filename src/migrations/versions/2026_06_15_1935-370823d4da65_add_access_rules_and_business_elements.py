"""Add access_rules and business_elements

Revision ID: 370823d4da65
Revises: 6905ff75904f
Create Date: 2026-06-15 19:35:51.251925

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "370823d4da65"
down_revision: Union[str, Sequence[str], None] = "6905ff75904f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "business_elements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.CheckConstraint("length(name) >= 1", name="business_element_name_check"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_business_elements_name"), "business_elements", ["name"], unique=True
    )
    op.create_table(
        "access_rules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("element_id", sa.Integer(), nullable=False),
        sa.Column(
            "create_permission",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "read_permission",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "read_all_permission",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "update_permission",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "update_all_permission",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "delete_permission",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "delete_all_permission",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["element_id"], ["business_elements.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("role_id", "element_id", name="unique_role_element_rule"),
    )

    op.bulk_insert(
        sa.table(
            "roles",
            sa.column("id", sa.Integer),
            sa.column("name", sa.String),
        ),
        [
            {"id": 1, "name": "Пользователь"},
            {"id": 2, "name": "Менеджер"},
            {"id": 3, "name": "Администратор"},
        ],
    )

    op.bulk_insert(
        sa.table(
            "business_elements",
            sa.column("id", sa.Integer),
            sa.column("name", sa.String),
        ),
        [
            {"id": 1, "name": "users"},
            {"id": 2, "name": "roles"},
            {"id": 3, "name": "business_elements"},
            {"id": 4, "name": "access_rules"},
            {"id": 5, "name": "reports"},
        ],
    )

    op.bulk_insert(
        sa.table(
            "access_rules",
            sa.column("id", sa.Integer),
            sa.column("role_id", sa.Integer),
            sa.column("element_id", sa.Integer),
            sa.column("create_permission", sa.Boolean),
            sa.column("read_permission", sa.Boolean),
            sa.column("read_all_permission", sa.Boolean),
            sa.column("update_permission", sa.Boolean),
            sa.column("update_all_permission", sa.Boolean),
            sa.column("delete_permission", sa.Boolean),
            sa.column("delete_all_permission", sa.Boolean),
        ),
        [
            {
                "id": 1,
                "role_id": 1,
                "element_id": 1,
                "create_permission": False,
                "read_permission": True,
                "read_all_permission": False,
                "update_permission": True,
                "update_all_permission": False,
                "delete_permission": True,
                "delete_all_permission": False,
            },
            {
                "id": 2,
                "role_id": 1,
                "element_id": 5,
                "create_permission": False,
                "read_permission": True,
                "read_all_permission": False,
                "update_permission": False,
                "update_all_permission": False,
                "delete_permission": False,
                "delete_all_permission": False,
            },
            {
                "id": 3,
                "role_id": 2,
                "element_id": 1,
                "create_permission": True,
                "read_permission": True,
                "read_all_permission": True,
                "update_permission": True,
                "update_all_permission": False,
                "delete_permission": False,
                "delete_all_permission": False,
            },
            {
                "id": 4,
                "role_id": 2,
                "element_id": 5,
                "create_permission": True,
                "read_permission": True,
                "read_all_permission": True,
                "update_permission": True,
                "update_all_permission": False,
                "delete_permission": False,
                "delete_all_permission": False,
            },
            {
                "id": 5,
                "role_id": 3,
                "element_id": 1,
                "create_permission": True,
                "read_permission": True,
                "read_all_permission": True,
                "update_permission": True,
                "update_all_permission": True,
                "delete_permission": True,
                "delete_all_permission": True,
            },
            {
                "id": 6,
                "role_id": 3,
                "element_id": 2,
                "create_permission": True,
                "read_permission": True,
                "read_all_permission": True,
                "update_permission": True,
                "update_all_permission": True,
                "delete_permission": True,
                "delete_all_permission": True,
            },
            {
                "id": 7,
                "role_id": 3,
                "element_id": 3,
                "create_permission": True,
                "read_permission": True,
                "read_all_permission": True,
                "update_permission": True,
                "update_all_permission": True,
                "delete_permission": True,
                "delete_all_permission": True,
            },
            {
                "id": 8,
                "role_id": 3,
                "element_id": 4,
                "create_permission": True,
                "read_permission": True,
                "read_all_permission": True,
                "update_permission": True,
                "update_all_permission": True,
                "delete_permission": True,
                "delete_all_permission": True,
            },
            {
                "id": 9,
                "role_id": 3,
                "element_id": 5,
                "create_permission": True,
                "read_permission": True,
                "read_all_permission": True,
                "update_permission": True,
                "update_all_permission": True,
                "delete_permission": True,
                "delete_all_permission": True,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("access_rules")
    op.drop_index(op.f("ix_business_elements_name"), table_name="business_elements")
    op.drop_table("business_elements")
