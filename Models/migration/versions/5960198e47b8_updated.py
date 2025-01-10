"""updated

Revision ID: 5960198e47b8
Revises: 326618a45fb9
Create Date: 2025-01-09 17:12:16.926330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5960198e47b8'
down_revision: Union[str, None] = '326618a45fb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('restaurant', 'name')
    op.drop_column('restaurant', 'full_adress')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurant', sa.Column('full_adress', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('restaurant', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###