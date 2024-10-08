"""create payment_transaction table

Revision ID: b9116f9b0921
Revises: 38911ac74a42
Create Date: 2021-03-07 10:27:01.663185

"""
from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = 'b9116f9b0921'
down_revision = '38911ac74a42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment_gateway',
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('payment_type',
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('payment_transaction',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), default=uuid.uuid4, nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('requester', sa.String(length=255), nullable=True),
    sa.Column('reference_id', sa.String(length=255), nullable=False),
    sa.Column('transaction_id', sa.String(length=255), nullable=False),
    sa.Column('payment_status', sa.Enum('none', 'pending', 'cancel', 'error', 'fail', 'success', name='paymentstatusenum'), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('model_type', sa.String(length=255), nullable=True),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.Column('response_code', sa.String(length=255), nullable=True),
    sa.Column('response_decision', sa.String(length=255), nullable=True),
    sa.Column('card_number', sa.String(length=20), nullable=True),
    sa.Column('card_expiry_date', sa.String(length=10), nullable=True),
    sa.Column('note', sa.String(length=255), nullable=True),
    sa.Column('dump_response', sa.Text(), nullable=True),
    sa.Column('custom_properties', sa.JSON(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.Column('payment_gateway', sa.String(length=50), nullable=True),
    sa.Column('payment_type', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['payment_gateway'], ['payment_gateway.name'], ),
    sa.ForeignKeyConstraint(['payment_type'], ['payment_type.name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('reference_id'),
    sa.UniqueConstraint('transaction_id')
    )
    op.create_index(op.f('ix_payment_transaction_reference_id'), 'payment_transaction', ['reference_id'], unique=True)
    op.create_index(op.f('ix_payment_transaction_transaction_id'), 'payment_transaction', ['transaction_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_payment_transaction_transaction_id'), table_name='payment_transaction')
    op.drop_index(op.f('ix_payment_transaction_reference_id'), table_name='payment_transaction')
    op.drop_table('payment_transaction')
    op.drop_table('payment_type')
    op.drop_table('payment_gateway')
    # ### end Alembic commands ###
