"""add few columns to the post table

Revision ID: 3dd5e2d0fd4e
Revises: 431678fe4212
Create Date: 2025-10-03 13:26:19.218117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dd5e2d0fd4e'
down_revision: Union[str, Sequence[str], None] = '431678fe4212'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column("posts",sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))

    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
