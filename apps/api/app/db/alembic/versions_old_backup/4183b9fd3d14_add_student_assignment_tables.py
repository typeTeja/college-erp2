"""add_student_assignment_tables

Revision ID: 4183b9fd3d14
Revises: 814b6588fd2a
Create Date: 2026-01-08 00:53:14.836147

Creates tables for student assignment to sections and labs
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '4183b9fd3d14'
down_revision: Union[str, None] = '814b6588fd2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create student_section_assignment table
    op.create_table(
        'student_section_assignment',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('section_id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('semester_no', sa.Integer(), nullable=False),
        sa.Column('assignment_type', sa.String(20), nullable=False, server_default='AUTO'),
        sa.Column('assigned_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('assigned_by', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['student_id'], ['student.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['section_id'], ['section.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['batch_id'], ['academic_batches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['assigned_by'], ['user.id'], ondelete='SET NULL'),
        sa.UniqueConstraint('student_id', 'batch_id', 'semester_no', name='uq_student_section_semester')
    )
    
    # Create student_lab_assignment table
    op.create_table(
        'student_lab_assignment',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('practical_batch_id', sa.Integer(), nullable=False),
        sa.Column('section_id', sa.Integer(), nullable=False),
        sa.Column('assignment_type', sa.String(20), nullable=False, server_default='AUTO'),
        sa.Column('assigned_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('assigned_by', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['student_id'], ['student.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['practical_batch_id'], ['practical_batch.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['section_id'], ['section.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['assigned_by'], ['user.id'], ondelete='SET NULL'),
        sa.UniqueConstraint('student_id', 'practical_batch_id', name='uq_student_lab')
    )
    
    # Add indexes for performance
    op.create_index('idx_section_assignment_student', 'student_section_assignment', ['student_id'])
    op.create_index('idx_section_assignment_section', 'student_section_assignment', ['section_id'])
    op.create_index('idx_section_assignment_batch', 'student_section_assignment', ['batch_id'])
    op.create_index('idx_lab_assignment_student', 'student_lab_assignment', ['student_id'])
    op.create_index('idx_lab_assignment_lab', 'student_lab_assignment', ['practical_batch_id'])
    op.create_index('idx_lab_assignment_section', 'student_lab_assignment', ['section_id'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_lab_assignment_section', table_name='student_lab_assignment')
    op.drop_index('idx_lab_assignment_lab', table_name='student_lab_assignment')
    op.drop_index('idx_lab_assignment_student', table_name='student_lab_assignment')
    op.drop_index('idx_section_assignment_batch', table_name='student_section_assignment')
    op.drop_index('idx_section_assignment_section', table_name='student_section_assignment')
    op.drop_index('idx_section_assignment_student', table_name='student_section_assignment')
    
    # Drop tables
    op.drop_table('student_lab_assignment')
    op.drop_table('student_section_assignment')
