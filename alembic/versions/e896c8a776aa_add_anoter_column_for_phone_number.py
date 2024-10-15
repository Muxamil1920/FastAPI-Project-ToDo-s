"""Add anoter column for phone number

Revision ID: e896c8a776aa
Revises: 
Create Date: 2024-10-15 00:05:46.851060

"""
from email.policy import default
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e896c8a776aa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Users', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('Users', 'phone_number')
