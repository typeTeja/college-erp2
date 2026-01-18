"""Revision ID: c0a1b2c3d4add
Revises: 5e8e21927d0f
Create Date: 2025-12-26 01:40:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c0a1b2c3d4add'
down_revision = '1ceeecea7e49'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'institute_info',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('short_code', sa.String(255), nullable=True),
        sa.Column('address', sa.String(255), nullable=True),
        sa.Column('contact_email', sa.String(255), nullable=True),
        sa.Column('contact_phone', sa.String(255), nullable=True),
        sa.Column('logo_url', sa.String(255), nullable=True),
    )

def downgrade():
    op.drop_table('institute_info')
