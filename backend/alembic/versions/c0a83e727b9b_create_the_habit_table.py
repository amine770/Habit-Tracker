"""create the habit table

Revision ID: c0a83e727b9b
Revises: f97d2c17d76d
Create Date: 2025-11-23 12:23:46.792690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.db.session import Base


# revision identifiers, used by Alembic.
revision: str = 'c0a83e727b9b'
down_revision: Union[str, Sequence[str], None] = 'f97d2c17d76d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("habits", 
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="cascade"), nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("frequency", sa.String, server_default="daily", nullable=False),
        sa.Column("color", sa.String, nullable=False, server_default="blue"),
        sa.Column("icon", sa.String, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=text("now()"), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("habits")
    pass
