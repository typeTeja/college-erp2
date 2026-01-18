"""create_batch_tables_with_auto_generation

Revision ID: 9e006e92bde2
Revises: d12c236e8a01
Create Date: 2026-01-05 22:53:00

Creates batch system tables:
- academic_batches
- program_years (READ-ONLY, auto-generated)
- batch_semesters (frozen from regulation)
- batch_subjects (frozen from regulation)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e006e92bde2'
down_revision: Union[str, None] = 'd12c236e8a01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create academic_batches table
    op.create_table(
        'academic_batches',
        sa.Column('id', sa.Integer(), nullable=False),
        
        # Batch identification
        sa.Column('batch_code', sa.String(length=50), nullable=False),
        sa.Column('batch_name', sa.String(length=100), nullable=False),
        
        # Links
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('regulation_id', sa.Integer(), nullable=False),
        
        # Academic years
        sa.Column('joining_year', sa.Integer(), nullable=False),
        sa.Column('start_year', sa.Integer(), nullable=False),
        sa.Column('end_year', sa.Integer(), nullable=False),
        
        # Current status
        sa.Column('current_year', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('total_students', sa.Integer(), nullable=False, server_default='0'),
        
        # Status
        sa.Column('status', sa.String(length=20), nullable=False, server_default='active'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['program_id'], ['program.id'], name='fk_batch_program'),
        sa.ForeignKeyConstraint(['regulation_id'], ['regulations.id'], name='fk_batch_regulation'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='fk_batch_created_by'),
        sa.UniqueConstraint('batch_code', name='uq_batch_code'),
        sa.UniqueConstraint('program_id', 'joining_year', name='uq_batch_program_year'),
        
        # Check constraints
        sa.CheckConstraint('current_year >= 1', name='ck_batch_current_year'),
        sa.CheckConstraint('total_students >= 0', name='ck_batch_total_students'),
        sa.CheckConstraint('joining_year >= 2000 AND joining_year <= 2100', name='ck_batch_joining_year'),
    )
    
    # Create indexes
    op.create_index('ix_academic_batches_batch_code', 'academic_batches', ['batch_code'], unique=True)
    op.create_index('ix_academic_batches_program_id', 'academic_batches', ['program_id'])
    op.create_index('ix_academic_batches_regulation_id', 'academic_batches', ['regulation_id'])
    
    # Create program_years table (SYSTEM-OWNED, READ-ONLY)
    op.create_table(
        'program_years',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('year_no', sa.Integer(), nullable=False),
        sa.Column('year_name', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['batch_id'], ['academic_batches.id'], name='fk_program_year_batch', ondelete='CASCADE'),
        
        # Check constraints
        sa.CheckConstraint('year_no >= 1 AND year_no <= 5', name='ck_program_year_no'),
    )
    
    # Create indexes
    op.create_index('ix_program_years_batch_id', 'program_years', ['batch_id'])
    
    # Create batch_semesters table
    op.create_table(
        'batch_semesters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('program_year_id', sa.Integer(), nullable=False),
        
        sa.Column('program_year', sa.Integer(), nullable=False),
        sa.Column('semester_no', sa.Integer(), nullable=False),
        sa.Column('semester_name', sa.String(length=50), nullable=False),
        
        # Credit requirements (frozen from regulation)
        sa.Column('total_credits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('min_credits_to_pass', sa.Integer(), nullable=False, server_default='0'),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['batch_id'], ['academic_batches.id'], name='fk_batch_semester_batch', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['program_year_id'], ['program_years.id'], name='fk_batch_semester_program_year', ondelete='CASCADE'),
        sa.UniqueConstraint('batch_id', 'semester_no', name='uq_batch_semester'),
        
        # Check constraints
        sa.CheckConstraint('program_year >= 1 AND program_year <= 5', name='ck_batch_semester_program_year'),
        sa.CheckConstraint('semester_no >= 1 AND semester_no <= 10', name='ck_batch_semester_no'),
        sa.CheckConstraint('total_credits >= 0', name='ck_batch_semester_total_credits'),
        sa.CheckConstraint('min_credits_to_pass >= 0', name='ck_batch_semester_min_credits'),
    )
    
    # Create indexes
    op.create_index('ix_batch_semesters_batch_id', 'batch_semesters', ['batch_id'])
    op.create_index('ix_batch_semesters_program_year_id', 'batch_semesters', ['program_year_id'])
    
    # Create batch_subjects table
    op.create_table(
        'batch_subjects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        
        # Subject identification (frozen)
        sa.Column('subject_code', sa.String(length=20), nullable=False),
        sa.Column('subject_name', sa.String(length=200), nullable=False),
        sa.Column('short_name', sa.String(length=50), nullable=False),
        
        # Subject type (frozen)
        sa.Column('subject_type', sa.String(length=20), nullable=False),
        
        # Semester placement (frozen)
        sa.Column('program_year', sa.Integer(), nullable=False),
        sa.Column('semester_no', sa.Integer(), nullable=False),
        
        # Marks structure (frozen)
        sa.Column('internal_max', sa.Integer(), nullable=False),
        sa.Column('external_max', sa.Integer(), nullable=False),
        sa.Column('total_max', sa.Integer(), nullable=False),
        sa.Column('passing_percentage', sa.Integer(), nullable=False, server_default='40'),
        
        # Evaluation configuration (frozen)
        sa.Column('evaluation_type', sa.String(length=30), nullable=False),
        sa.Column('has_exam', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('has_assignments', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('hours_per_session', sa.Integer(), nullable=False, server_default='1'),
        
        # Credits (frozen)
        sa.Column('credits', sa.Integer(), nullable=False),
        
        # Status
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('is_elective', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['batch_id'], ['academic_batches.id'], name='fk_batch_subject_batch', ondelete='CASCADE'),
        sa.UniqueConstraint('batch_id', 'subject_code', name='uq_batch_subject'),
        
        # Check constraints
        sa.CheckConstraint('program_year >= 1 AND program_year <= 5', name='ck_batch_subject_program_year'),
        sa.CheckConstraint('semester_no >= 1 AND semester_no <= 10', name='ck_batch_subject_semester_no'),
        sa.CheckConstraint('internal_max >= 0', name='ck_batch_subject_internal_max'),
        sa.CheckConstraint('external_max >= 0', name='ck_batch_subject_external_max'),
        sa.CheckConstraint('total_max >= 0', name='ck_batch_subject_total_max'),
        sa.CheckConstraint('passing_percentage >= 0 AND passing_percentage <= 100', name='ck_batch_subject_passing_pct'),
        sa.CheckConstraint('hours_per_session >= 0', name='ck_batch_subject_hours'),
        sa.CheckConstraint('credits >= 0', name='ck_batch_subject_credits'),
    )
    
    # Create indexes
    op.create_index('ix_batch_subjects_batch_id', 'batch_subjects', ['batch_id'])
    op.create_index('ix_batch_subjects_subject_code', 'batch_subjects', ['subject_code'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('ix_batch_subjects_subject_code', table_name='batch_subjects')
    op.drop_index('ix_batch_subjects_batch_id', table_name='batch_subjects')
    op.drop_table('batch_subjects')
    
    op.drop_index('ix_batch_semesters_program_year_id', table_name='batch_semesters')
    op.drop_index('ix_batch_semesters_batch_id', table_name='batch_semesters')
    op.drop_table('batch_semesters')
    
    op.drop_index('ix_program_years_batch_id', table_name='program_years')
    op.drop_table('program_years')
    
    op.drop_index('ix_academic_batches_regulation_id', table_name='academic_batches')
    op.drop_index('ix_academic_batches_program_id', table_name='academic_batches')
    op.drop_index('ix_academic_batches_batch_code', table_name='academic_batches')
    op.drop_table('academic_batches')
