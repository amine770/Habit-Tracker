"""add username column in the user tabel

Revision ID: f97d2c17d76d
Revises: 89a5a41ff301
Create Date: 2025-11-22 12:08:50.486536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f97d2c17d76d'
down_revision: Union[str, Sequence[str], None] = '89a5a41ff301'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users",
                  sa.Column("username", sa.String, nullable=False)
                  )
    pass


def downgrade() -> None:
    op.drop_column("users", "username")
    pass
