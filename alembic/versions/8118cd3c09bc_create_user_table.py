"""create user table

Revision ID: 8118cd3c09bc
Revises: 
Create Date: 2023-11-19 19:12:51.973073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8118cd3c09bc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('username', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), 
        sa.Column('telegram_user_id', sa.Integer(), nullable=True), sa.Column('instagram_username', sa.String(), nullable=True))



def downgrade() -> None:
    op.drop_table('users')
