
"""add cancelled approval decision

Revision ID: 163879dbc997
Revises: 80d80b965bc4
Create Date: 2026-11-16 13:33:58.895155

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "163879dbc997"
down_revision: Union[str, Sequence[str], None] = "80d80b965bc4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add CANCELLED to the approval_decision PostgreSQL enum."""

    op.execute(
        "ALTER TYPE approval_decision ADD VALUE IF NOT EXISTS 'CANCELLED'"
    )


def downgrade() -> None:
    """
    PostgreSQL does not support directly removing an enum value.

    The CANCELLED value is intentionally retained on downgrade.
    """
    pass
