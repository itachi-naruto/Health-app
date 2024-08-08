"""create insert Roles table

Revision ID: bdc4689515e5
Revises: 891daad15318
Create Date: 2021-02-26 11:02:28.886172

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa
from werkzeug.security import generate_password_hash
import uuid
from config import BaseConfig


# revision identifiers, used by Alembic.
revision = 'bdc4689515e5'
down_revision = '891daad15318'
branch_labels = None
depends_on = None

# Create an ad-hoc table to use for the insert statement.
users_table = sa.table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), server_default='', nullable=False),
    sa.Column('public_id', sa.String(length=255), nullable=True),
)
roles_table = sa.table('roles',
    sa.column('id', sa.Integer()),
    sa.column('name', sa.String),
)
user_roles_table = sa.table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
)


def upgrade():
    hash_pass = generate_password_hash('123', method=BaseConfig.HASH_METHOD)
    op.bulk_insert(users_table,
     [
         {'id':1, 'is_active':1, 'phone':999, 'email':'info@smartlaboman.com',
         'password': hash_pass, 'public_id': str(uuid.uuid4())}
     ]
     )
    op.bulk_insert(roles_table,
    [
        {'id':1, 'name':'Admin'},
        {'id':2, 'name':'Center'},
        {'id':3, 'name':'Doctor'},
        {'id':4, 'name':'Manager'},
        {'id':5, 'name':'Patient'}
    ]
    )
    op.bulk_insert(user_roles_table,
    [
        {'id':1, 'user_id':1, 'role_id':1}
    ]
    )



def downgrade():
    pass