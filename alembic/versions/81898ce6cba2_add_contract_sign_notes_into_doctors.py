"""add contract_sign,notes into doctors

Revision ID: 81898ce6cba2
Revises: 91fad7ca90bd
Create Date: 2023-08-25 10:06:44.929641

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81898ce6cba2'
down_revision = '91fad7ca90bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contract_sign', sa.Boolean(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('notes', sa.String(length=1000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.drop_column('notes')
        batch_op.drop_column('contract_sign')

    # ### end Alembic commands ###
