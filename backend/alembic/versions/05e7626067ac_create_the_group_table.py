"""create the group table

Revision ID: 05e7626067ac
Revises: 818d7c4dca78
Create Date: 2025-11-30 14:51:51.272815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05e7626067ac'
down_revision: Union[str, Sequence[str], None] = '818d7c4dca78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("groups",
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                    sa.Column("name", sa.String, unique=True, nullable=False),
                    sa.Column("description", sa.Text, nullable=False),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="cascade"), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table("groups")
