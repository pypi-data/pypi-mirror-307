"""add logo_url

Revision ID: 531dff33369c
Revises: 8b4e2235b960
Create Date: 2023-08-02 08:29:02.252811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '531dff33369c'
down_revision = '8b4e2235b960'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('customer', sa.Column('logo_url', sa.String(length=254), nullable=True))
    op.add_column('user_pref', sa.Column('logo_url', sa.String(length=254), nullable=True))


def downgrade() -> None:
    op.drop_column('user_pref', 'logo_url')
    op.drop_column('customer', 'logo_url')
