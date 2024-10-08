"""add vat to payment_transaction table

Revision ID: cd6c451a22de
Revises: 8e173d4598c1
Create Date: 2021-04-27 14:24:03.130323

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd6c451a22de'
down_revision = '8e173d4598c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment_transaction', sa.Column('vat', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payment_transaction', 'vat')
    # ### end Alembic commands ###
