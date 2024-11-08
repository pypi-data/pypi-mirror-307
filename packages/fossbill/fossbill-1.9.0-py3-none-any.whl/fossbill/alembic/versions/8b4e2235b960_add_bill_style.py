"""add bill_style

Revision ID: 8b4e2235b960
Revises: ac14f3a73a29
Create Date: 2023-07-31 12:09:24.058838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b4e2235b960'
down_revision = 'ac14f3a73a29'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user_pref', sa.Column('bill_style', sa.String(length=1500), nullable=True))


def downgrade() -> None:
    op.drop_column('user_pref', 'bill_style')
