"""add content column to post table

Revision ID: 1e96bf9f918e
Revises: 6e0dbb924374
Create Date: 2025-10-02 14:38:57.768751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e96bf9f918e'
down_revision: Union[str, Sequence[str], None] = '6e0dbb924374'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
