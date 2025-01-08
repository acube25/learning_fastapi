"""add last few columns to post table

Revision ID: c7b117b950ab
Revises: e2d6f11ddad0
Create Date: 2025-01-07 13:43:25.487795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7b117b950ab'
down_revision: Union[str, None] = 'e2d6f11ddad0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, 
                            server_default=sa.text("NOW()")),)
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
