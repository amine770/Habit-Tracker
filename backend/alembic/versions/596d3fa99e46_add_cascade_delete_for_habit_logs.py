"""add cascade delete for habit logs

Revision ID: 596d3fa99e46
Revises: ba6aa23e46c0
Create Date: 2025-12-01 20:55:29.852200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '596d3fa99e46'
down_revision: Union[str, Sequence[str], None] = 'ba6aa23e46c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
