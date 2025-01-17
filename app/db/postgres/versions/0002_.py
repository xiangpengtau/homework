"""

Revision ID: 0002
Revises: 0001
Create Date: 2024-11-09 16:52:35.835058

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('chief', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group', 'chief')
    # ### end Alembic commands ###
