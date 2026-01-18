"""add_academic_indexes_and_improve_performance

Revision ID: 814b6588fd2a
Revises: f01ba63fccbd
Create Date: 2026-01-08 00:40:51.520434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '814b6588fd2a'
down_revision: Union[str, None] = 'f01ba63fccbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add index on section.batch_id for faster batch-level queries
    op.create_index(
        'idx_section_batch_id',
        'section',
        ['batch_id'],
        unique=False
    )
    
    # Add index on batch_semesters.batch_id for hierarchy queries
    op.create_index(
        'idx_batch_semester_batch_id',
        'batch_semesters',
        ['batch_id'],
        unique=False
    )
    
    # Add index on program_years.batch_id for year lookups
    op.create_index(
        'idx_program_year_batch_id',
        'program_years',
        ['batch_id'],
        unique=False
    )


def downgrade() -> None:
    # Remove indexes in reverse order
    op.drop_index('idx_program_year_batch_id', table_name='program_years')
    op.drop_index('idx_batch_semester_batch_id', table_name='batch_semesters')
    op.drop_index('idx_section_batch_id', table_name='section')
