"""Initial migration

Revision ID: aac83f3ac440
Revises: 
Create Date: 2025-01-09 17:10:37.422358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aac83f3ac440'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('pidr', sa.Integer(), nullable=True))
    op.drop_column('location', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('location', 'pidr')
    # ### end Alembic commands ###
