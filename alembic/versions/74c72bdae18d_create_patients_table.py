"""create patients table

Revision ID: 74c72bdae18d
Revises: c4e979aa8653
Create Date: 2021-02-21 15:41:40.867300

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '74c72bdae18d'
down_revision = 'c4e979aa8653'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'patients',
        sa.Column('id',sa.Integer, primary_key=True),
        sa.Column('first_name',sa.String(255), nullable=False, server_default=''),
        sa.Column('last_name',sa.String(255), nullable=False, server_default=''),
        sa.Column('gender',sa.String(length=100)),
        sa.Column('birth_date',sa.DATE),
        sa.Column('blood_type',sa.String(length=100)),
        sa.Column('country',sa.String(length=100), server_default='OM'),
        sa.Column('user_id',sa.Integer, ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('parent_id', sa.Integer, ForeignKey('patients.id'), nullable=True),
    )

def downgrade():
    op.drop_table('patients')
