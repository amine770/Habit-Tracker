"""create users table

Revision ID: 89a5a41ff301
Revises: 43106a194eca
Create Date: 2025-11-21 17:20:09.630479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = '89a5a41ff301'
down_revision: Union[str, Sequence[str], None] = '43106a194eca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                sa.Column("id", sa.Integer, nullable=False, primary_key=True ),
                sa.Column("email", sa.String, nullable=False, unique=True),
                sa.Column("hashed_password", sa.String, nullable=False),
                sa.Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
                )
    pass

def downgrade() -> None:
    op.drop_table("users")
    pass
