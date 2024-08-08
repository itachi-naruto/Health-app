"""create doctors table

Revision ID: 1ac0b366e975
Revises: 74c72bdae18d
Create Date: 2021-02-21 15:41:43.790567

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '1ac0b366e975'
down_revision = '74c72bdae18d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'doctors',
        sa.Column('id',sa.Integer, primary_key=True),
        sa.Column('first_name',sa.String(255), nullable=False, server_default=''),
        sa.Column('last_name',sa.String(255), nullable=False, server_default=''),
        sa.Column('gender',sa.String(length=100)),
        sa.Column('birth_date',sa.DATE),
        sa.Column('blood_type',sa.String(length=100)),
        sa.Column('country',sa.String(length=100), server_default='OM'),
        sa.Column('address',sa.String(length=500)),
        sa.Column('place_location',sa.String(length=100)),
        sa.Column('exact_location',sa.String(length=100)),
        sa.Column('speciality',sa.JSON),
        sa.Column('professional_experiance',sa.String(length=100)),
        sa.Column('certification',sa.JSON),
        sa.Column('experiance',sa.String(length=100)),
        sa.Column('education',sa.JSON),
        sa.Column('memberships',sa.JSON),
        sa.Column('follow_up_fee',sa.Numeric(10,3)),
        sa.Column('consultation_fee',sa.Numeric(10,3)),
        sa.Column('biography',sa.String(length=255)),
        sa.Column('medical_board_registrations',sa.JSON),
        sa.Column('know_languages',sa.JSON),
        sa.Column('user_id',sa.Integer, ForeignKey('users.id', ondelete='CASCADE')),
    )


def downgrade():
    op.drop_table('doctors')
