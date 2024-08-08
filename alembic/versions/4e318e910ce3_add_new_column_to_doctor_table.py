"""add new column to doctor table

Revision ID: 4e318e910ce3
Revises: c5da3a7ceb6b
Create Date: 2021-02-26 10:04:34.883929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e318e910ce3'
down_revision = 'c5da3a7ceb6b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('doctors', sa.Column('is_approved', sa.Boolean(), nullable=False, server_default='0'))


def downgrade():
    op.drop_column('doctors', 'is_approved')
