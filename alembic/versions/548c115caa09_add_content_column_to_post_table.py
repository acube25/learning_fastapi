"""add content column to post table

Revision ID: 548c115caa09
Revises: 92feef9a0969
Create Date: 2025-01-07 13:22:37.829338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '548c115caa09'
down_revision: Union[str, None] = '92feef9a0969'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass