"""create centers table

Revision ID: 891daad15318
Revises: 4e318e910ce3
Create Date: 2021-02-26 10:30:29.178339

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '891daad15318'
down_revision = '4e318e910ce3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'centers',
        sa.Column('id',sa.Integer, primary_key=True),
        sa.Column('name',sa.String(255), nullable=False, server_default=''),
        sa.Column('country',sa.String(length=100), server_default='OM'),
        sa.Column('address',sa.String(length=500)),
        sa.Column('place_location',sa.String(length=100)),
        sa.Column('exact_location',sa.String(length=100)),
        sa.Column('user_id',sa.Integer, ForeignKey('users.id', ondelete='CASCADE'))
    )

def downgrade():
    op.drop_table('centers')
