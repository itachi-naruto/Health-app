"""create media table

Revision ID: c5da3a7ceb6b
Revises: 1ac0b366e975
Create Date: 2021-02-21 15:41:47.043923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5da3a7ceb6b'
down_revision = '1ac0b366e975'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'media',
        sa.Column('id',sa.Integer, primary_key=True, nullable=False),
        sa.Column('model_type',sa.String(length=255)),
        sa.Column('model_id',sa.Integer),
        sa.Column('collection_name',sa.String(length=255)),
        sa.Column('name',sa.String(length=255)),
        sa.Column('mime_type',sa.String(length=255)),
        sa.Column('disk',sa.String(length=255)),
        sa.Column('size',sa.String(length=255)),
        sa.Column('order_column',sa.Integer),
        sa.Column('upload_file',sa.String(length=255)),
        sa.Column('custom_properties',sa.JSON),
        sa.Column('create_date',sa.DateTime),
        sa.Column('last_modified',sa.DateTime),
    )


def downgrade():
    op.drop_table('media')
