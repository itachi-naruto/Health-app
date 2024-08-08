"""add column to doctor table

Revision ID: 66f646e52ee3
Revises: 08849e0bc188
Create Date: 2021-03-23 10:52:55.781080

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66f646e52ee3'
down_revision = '08849e0bc188'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doctors', sa.Column('image', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('doctors', 'image')
    # ### end Alembic commands ###
