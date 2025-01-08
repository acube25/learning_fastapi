"""create posts table

Revision ID: 92feef9a0969
Revises: 
Create Date: 2025-01-07 13:16:44.123191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92feef9a0969'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable = False, primary_key = True), 
                    sa.Column("title", sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass