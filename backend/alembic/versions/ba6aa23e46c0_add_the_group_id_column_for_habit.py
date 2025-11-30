"""add the group.id column for habit

Revision ID: ba6aa23e46c0
Revises: 05e7626067ac
Create Date: 2025-11-30 14:55:18.016697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba6aa23e46c0'
down_revision: Union[str, Sequence[str], None] = '05e7626067ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("habits",
                  sa.Column("group_id", 
                        sa.Integer, 
                        sa.ForeignKey("groups.id", ondelete="cascade"), 
                        nullable=True)
                  )    


def downgrade() -> None:
    op.drop_column("habits", "group_id")
