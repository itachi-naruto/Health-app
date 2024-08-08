"""alter patients table

Revision ID: d865e36f24e0
Revises: 934d06a736e5
Create Date: 2024-05-26 15:41:31.182022

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd865e36f24e0'
down_revision = '934d06a736e5'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('patients', sa.Column('civil_id', sa.String(length=10), server_default='', nullable=False)),
     op.add_column('patients', sa.Column('address', sa.String(length=300), server_default='', nullable=True)),

def downgrade():
    op.drop_column('patients', 'civil_id'),
    op.drop_column('patients', 'address'),
