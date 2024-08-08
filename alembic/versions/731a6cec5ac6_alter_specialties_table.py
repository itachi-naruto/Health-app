"""alter specialties table

Revision ID: 731a6cec5ac6
Revises: d865e36f24e0
Create Date: 2024-05-30 16:40:51.164738

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '731a6cec5ac6'
down_revision = 'd865e36f24e0'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('specialties', sa.Column('image', sa.String(length=300), server_default='', nullable=False)),
     op.add_column('specialties', sa.Column('name_ar', sa.String(length=255), server_default='', nullable=True)),

def downgrade():
    op.drop_column('specialties', 'image'),
    op.drop_column('specialties', 'name_ar'),
