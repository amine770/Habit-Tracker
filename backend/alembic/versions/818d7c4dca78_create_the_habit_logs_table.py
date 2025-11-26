"""create the habit logs table

Revision ID: 818d7c4dca78
Revises: c0a83e727b9b
Create Date: 2025-11-26 17:51:38.808605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '818d7c4dca78'
down_revision: Union[str, Sequence[str], None] = 'c0a83e727b9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("habit_logs",
                    sa.Column("id",sa.Integer, nullable=False, primary_key=True),
                    sa.Column("habit_id", sa.Integer, sa.ForeignKey("habits.id", ondelete="cascade"), nullable=False),
                    sa.Column("completed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
                    sa.Column("notes", sa.Text, nullable=True)
                    )


def downgrade() -> None:
    op.drop_table("habit_logs")
