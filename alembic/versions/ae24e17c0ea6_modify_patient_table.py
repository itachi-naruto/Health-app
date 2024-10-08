"""modify patient table

Revision ID: ae24e17c0ea6
Revises: 357918b7e751
Create Date: 2021-04-19 09:53:10.847680

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae24e17c0ea6'
down_revision = '357918b7e751'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patients', sa.Column('relation', sa.String(length=100), server_default='', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patients', 'relation')
    # ### end Alembic commands ###
