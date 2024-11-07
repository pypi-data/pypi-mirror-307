"""add user free

Revision ID: e73b0c0cdf0b
Revises: 531dff33369c
Create Date: 2023-08-11 16:10:43.272415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e73b0c0cdf0b'
down_revision = '531dff33369c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('free', sa.Boolean(), server_default='FALSE', nullable=False))


def downgrade() -> None:
    op.drop_column('user', 'free')
