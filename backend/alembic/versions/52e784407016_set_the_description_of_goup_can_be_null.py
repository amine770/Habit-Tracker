"""set the description of goup can be null 

Revision ID: 52e784407016
Revises: 596d3fa99e46
Create Date: 2025-12-01 21:32:53.139111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52e784407016'
down_revision: Union[str, Sequence[str], None] = '596d3fa99e46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
