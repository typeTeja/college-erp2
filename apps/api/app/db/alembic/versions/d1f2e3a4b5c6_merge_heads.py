"""Revision ID: d1f2e3a4b5c6
Revises: 1ceeecea7e49, c0a1b2c3d4add
Create Date: 2025-12-26 02:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd1f2e3a4b5c6'
down_revision = ('1ceeecea7e49', 'c0a1b2c3d4add')
branch_labels = None
depends_on = None

def upgrade():
    # No schema changes – this is a merge point for multiple heads.
    pass

def downgrade():
    # No schema changes to revert.
    pass
