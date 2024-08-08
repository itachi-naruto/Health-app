"""create users table

Revision ID: c4e979aa8653
Revises: 
Create Date: 2021-02-21 15:41:36.672623

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = 'c4e979aa8653'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id',sa.Integer, primary_key=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('phone',sa.Integer, nullable=False, unique=True),
        sa.Column('email',sa.String(255), nullable=False, unique=True),
        sa.Column('mobile_confirmed_at',sa.DateTime()),
        sa.Column('email_confirmed_at',sa.DateTime()),
        sa.Column('password',sa.String(255), nullable=False, server_default=''),
        sa.Column('public_id',sa.String(length=255)),
    )
    op.create_table(
        'roles',
        sa.Column('id',sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), unique=True)
    )
    op.create_table(
        'user_roles',
        sa.Column('id',sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer,ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('role_id', sa.Integer, ForeignKey('roles.id', ondelete='CASCADE'))
    )
    op.create_table(
        'login_tracking',
        sa.Column('id',sa.Integer, primary_key=True),
        sa.Column('date' ,sa.DateTime()),
        sa.Column('status' ,sa.String(length=255)),
        sa.Column('others' ,sa.String(length=255), server_default=None),
        sa.Column('user_id', sa.Integer, ForeignKey('users.id', ondelete='CASCADE'))
    )

def downgrade():
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('user_roles')
    op.drop_table('login_tracking')
