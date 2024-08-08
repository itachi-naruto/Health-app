"""create setting table

Revision ID: c83f038a5807
Revises: b9116f9b0921
Create Date: 2021-03-10 09:34:27.895000

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c83f038a5807'
down_revision = 'b9116f9b0921'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_setting',
    sa.Column('key', sa.String(length=10), nullable=False),
    sa.Column('category', sa.String(length=10), nullable=True),
    sa.Column('value', sa.String(length=255), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('key')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('app_setting')
    # ### end Alembic commands ###
