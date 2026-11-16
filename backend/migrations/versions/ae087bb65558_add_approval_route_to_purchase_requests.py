
"""add approval route to purchase requests

Revision ID: ae087bb65558
Revises: 28582772d777
Create Date: 2026-11-13 13:36:54.153335

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'ae087bb65558'
down_revision: Union[str, Sequence[str], None] = '28582772d777'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


approval_route_enum = postgresql.ENUM(
    'AUTOMATIC_ELIGIBILITY',
    'MANAGER',
    'MANAGER_AND_FINANCE',
    name='approval_route',
    create_type=False,
)


def upgrade() -> None:
    """Add approval routing to existing purchase requests."""

    # 1. Create the PostgreSQL enum type.
    approval_route_enum.create(op.get_bind(), checkfirst=True)

    # 2. Add the new column temporarily as nullable.
    op.add_column(
        'purchase_requests',
        sa.Column(
            'approval_route',
            approval_route_enum,
            nullable=True,
        ),
    )

    # 3. Assign an approval route to existing records.
    # Existing requests are classified using their purchase amount.
    op.execute(
        """
        UPDATE purchase_requests
        SET approval_route = CASE
            WHEN amount < 2000
                THEN 'AUTOMATIC_ELIGIBILITY'::approval_route
            WHEN amount < 20000
                THEN 'MANAGER'::approval_route
            ELSE 'MANAGER_AND_FINANCE'::approval_route
        END
        """
    )

    # 4. Require an approval route for all future records.
    op.alter_column(
        'purchase_requests',
        'approval_route',
        existing_type=approval_route_enum,
        nullable=False,
    )


def downgrade() -> None:
    """Remove approval routing."""

    # 1. Remove the column.
    op.drop_column('purchase_requests', 'approval_route')

    # 2. Remove the PostgreSQL enum type.
    approval_route_enum.drop(op.get_bind(), checkfirst=True)
