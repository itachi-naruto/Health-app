"""alter user table add otp

Revision ID: 2c7384d781ae
Revises: 731a6cec5ac6
Create Date: 2024-06-10 16:07:48.458944

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c7384d781ae'
down_revision = '731a6cec5ac6'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('users', sa.Column('otp', sa.String(length=6), server_default='', nullable=True)),
     op.add_column('users', sa.Column('expiration_time', sa.DateTime, nullable=True)),
     op.add_column('users', sa.Column('has_profile', sa.Boolean(), server_default='0', nullable=False))

def downgrade():
    op.drop_column('users', 'otp'),
    op.drop_column('users', 'expiration_time'),
    op.drop_column('users', 'has_profile')

