"""Add current_step manual

Revision ID: f33333333333
Revises: 3662506e5c44
Create Date: 2026-02-08 10:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = 'f33333333333'
down_revision = '3662506e5c44'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('application', sa.Column('current_step', sa.Integer(), nullable=True))
    op.add_column('application', sa.Column('last_saved_at', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('application', 'last_saved_at')
    op.drop_column('application', 'current_step')
