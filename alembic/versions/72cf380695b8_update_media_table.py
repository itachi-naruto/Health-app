"""update media table

Revision ID: 72cf380695b8
Revises: dc35f0f022bf
Create Date: 2022-08-16 11:11:15.665346

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa
from depot.fields.sqlalchemy import UploadedFileField
import uuid

# revision identifiers, used by Alembic.
revision = '72cf380695b8'
down_revision = 'dc35f0f022bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file', UploadedFileField(), nullable=True))
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               type_=sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4,
               existing_nullable=False)
        batch_op.drop_column('upload_file')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.add_column(sa.Column('upload_file', sa.VARCHAR(length=255), nullable=True))
        batch_op.alter_column('id',
               existing_type=sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4,
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.drop_column('file')

    # ### end Alembic commands ###
