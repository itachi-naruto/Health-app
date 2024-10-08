"""Initial migration for Oman geodata tables

Revision ID: ef48670d6ddb
Revises: 2c7384d781ae
Create Date: 2024-06-27 04:35:07.153955

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ef48670d6ddb'
down_revision = '2c7384d781ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointments', 'symptoms',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=512),
               nullable=True)
    op.drop_constraint('centers_ibfk_1', 'centers', type_='foreignkey')
    op.create_foreign_key(None, 'centers', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.alter_column('patients', 'civil_id',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=10),
               nullable=False,
               existing_server_default=sa.text("''"))


    op.alter_column('specialties', 'name_ar',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=150),
               type_=sa.String(length=255),
               nullable=False,
               existing_server_default=sa.text("''"))
    op.alter_column('specialties', 'image',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=300),
               type_=sa.String(length=100),
               nullable=True,
               existing_server_default=sa.text("''"))


    op.create_table('governorate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wilayat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('governorate_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['governorate_id'], ['governorate.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('wilayat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['wilayat_id'], ['wilayat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.alter_column('specialties', 'image',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=300),
               nullable=False,
               existing_server_default=sa.text("''"))
    op.alter_column('specialties', 'name_ar',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=150),
               nullable=True,
               existing_server_default=sa.text("''"))


    op.alter_column('patients', 'civil_id',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=10),
               nullable=True,
               existing_server_default=sa.text("''"))
    op.drop_constraint(None, 'centers', type_='foreignkey')
    op.create_foreign_key('centers_ibfk_1', 'centers', 'users', ['user_id'], ['id'])
    op.alter_column('appointments', 'symptoms',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=512),
               nullable=False)
    op.drop_table('area')
    op.drop_table('wilayat')
    op.drop_table('governorate')
    # ### end Alembic commands ###
