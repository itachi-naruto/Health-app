"""modify centers table

Revision ID: 934d06a736e5
Revises: d93f35705bfe
Create Date: 2024-03-03 18:05:08.019793

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '934d06a736e5'
down_revision = 'd93f35705bfe'
branch_labels = None
depends_on = None


def upgrade():
    # Use batch mode for compatibility with SQLite and other databases
    with op.batch_alter_table('centers', schema=None) as batch_op:
        batch_op.alter_column('speciality',
                              existing_type=sa.String(length=255),
                              nullable=True)
        batch_op.alter_column('description',
                              existing_type=sa.String(length=500),
                              nullable=True)
        batch_op.alter_column('start',
                              existing_type=sa.String(length=100),
                              nullable=True)
        batch_op.alter_column('end',
                              existing_type=sa.String(length=100),
                              nullable=True)


def downgrade():
    # Reverse the changes made in upgrade()
    with op.batch_alter_table('centers', schema=None) as batch_op:
        batch_op.alter_column('speciality',
                              existing_type=sa.String(length=255),
                              nullable=False)
        batch_op.alter_column('description',
                              existing_type=sa.String(length=500),
                              nullable=False)
        batch_op.alter_column('start',
                              existing_type=sa.String(length=100),
                              nullable=False)
        batch_op.alter_column('end',
                              existing_type=sa.String(length=100),
                              nullable=False)