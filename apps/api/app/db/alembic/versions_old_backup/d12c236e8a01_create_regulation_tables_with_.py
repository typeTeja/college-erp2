"""create_regulation_tables_with_constraints

Revision ID: d12c236e8a01
Revises: 5e4c401dd090
Create Date: 2026-01-05 22:39:00

Creates regulation system tables with PostgreSQL constraints:
- regulations
- regulation_subjects
- regulation_semesters
- regulation_promotion_rules
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd12c236e8a01'
down_revision: Union[str, None] = '5e4c401dd090'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create regulations table
    op.create_table(
        'regulations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('regulation_code', sa.String(length=20), nullable=False),
        sa.Column('regulation_name', sa.String(length=100), nullable=False),
        sa.Column('program_id', sa.Integer(), nullable=False),
        
        # Promotion model
        sa.Column('promotion_model', sa.String(length=50), nullable=False, server_default='CREDIT_BASED'),
        
        # Promotion percentages
        sa.Column('year1_to_year2_min_percentage', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('year2_to_year3_min_year2_percentage', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('year3_to_graduation_min_percentage', sa.Integer(), nullable=False, server_default='100'),
        
        # Passing marks
        sa.Column('min_internal_pass', sa.Integer(), nullable=False, server_default='12'),
        sa.Column('min_external_pass', sa.Integer(), nullable=False, server_default='28'),
        sa.Column('min_total_pass', sa.Integer(), nullable=False, server_default='40'),
        
        # Locking mechanism
        sa.Column('is_locked', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('locked_at', sa.DateTime(), nullable=True),
        sa.Column('locked_by', sa.Integer(), nullable=True),
        
        # Optimistic locking
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        
        # Status
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['program_id'], ['program.id'], name='fk_regulation_program'),
        sa.ForeignKeyConstraint(['locked_by'], ['user.id'], name='fk_regulation_locked_by'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='fk_regulation_created_by'),
        sa.ForeignKeyConstraint(['updated_by'], ['user.id'], name='fk_regulation_updated_by'),
        
        # Check constraints for percentages
        sa.CheckConstraint('year1_to_year2_min_percentage >= 0 AND year1_to_year2_min_percentage <= 100', name='ck_year1_to_year2_pct'),
        sa.CheckConstraint('year2_to_year3_min_year2_percentage >= 0 AND year2_to_year3_min_year2_percentage <= 100', name='ck_year2_to_year3_pct'),
        sa.CheckConstraint('year3_to_graduation_min_percentage >= 0 AND year3_to_graduation_min_percentage <= 100', name='ck_year3_to_grad_pct'),
        sa.CheckConstraint('min_internal_pass >= 0', name='ck_min_internal_pass'),
        sa.CheckConstraint('min_external_pass >= 0', name='ck_min_external_pass'),
        sa.CheckConstraint('min_total_pass >= 0', name='ck_min_total_pass'),
    )
    
    # Create indexes
    op.create_index('ix_regulations_regulation_code', 'regulations', ['regulation_code'], unique=True)
    op.create_index('ix_regulations_program_id', 'regulations', ['program_id'])
    op.create_index('ix_regulations_is_locked', 'regulations', ['is_locked'])
    op.create_index('ix_regulations_is_active', 'regulations', ['is_active'])
    
    # Create regulation_subjects table
    op.create_table(
        'regulation_subjects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('regulation_id', sa.Integer(), nullable=False),
        
        # Subject identification
        sa.Column('subject_code', sa.String(length=20), nullable=False),
        sa.Column('subject_name', sa.String(length=200), nullable=False),
        sa.Column('short_name', sa.String(length=50), nullable=False),
        
        # Subject type
        sa.Column('subject_type', sa.String(length=20), nullable=False),
        
        # Semester placement
        sa.Column('program_year', sa.Integer(), nullable=False),
        sa.Column('semester_no', sa.Integer(), nullable=False),
        
        # Marks structure
        sa.Column('internal_max', sa.Integer(), nullable=False),
        sa.Column('external_max', sa.Integer(), nullable=False),
        sa.Column('total_max', sa.Integer(), nullable=False),
        sa.Column('passing_percentage', sa.Integer(), nullable=False, server_default='40'),
        
        # Evaluation configuration
        sa.Column('evaluation_type', sa.String(length=30), nullable=False),
        sa.Column('has_exam', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('has_assignments', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('hours_per_session', sa.Integer(), nullable=False, server_default='1'),
        
        # Credits
        sa.Column('credits', sa.Integer(), nullable=False),
        
        # Status
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('is_elective', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['regulation_id'], ['regulations.id'], name='fk_regulation_subject_regulation', ondelete='CASCADE'),
        sa.UniqueConstraint('regulation_id', 'subject_code', name='uq_regulation_subject'),
        
        # Check constraints
        sa.CheckConstraint('program_year >= 1 AND program_year <= 5', name='ck_subject_program_year'),
        sa.CheckConstraint('semester_no >= 1 AND semester_no <= 10', name='ck_subject_semester_no'),
        sa.CheckConstraint('internal_max >= 0', name='ck_subject_internal_max'),
        sa.CheckConstraint('external_max >= 0', name='ck_subject_external_max'),
        sa.CheckConstraint('total_max >= 0', name='ck_subject_total_max'),
        sa.CheckConstraint('passing_percentage >= 0 AND passing_percentage <= 100', name='ck_subject_passing_pct'),
        sa.CheckConstraint('hours_per_session >= 0', name='ck_subject_hours'),
        sa.CheckConstraint('credits >= 0', name='ck_subject_credits'),
    )
    
    # Create indexes
    op.create_index('ix_regulation_subjects_regulation_id', 'regulation_subjects', ['regulation_id'])
    op.create_index('ix_regulation_subjects_subject_code', 'regulation_subjects', ['subject_code'])
    
    # Create regulation_semesters table
    op.create_table(
        'regulation_semesters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('regulation_id', sa.Integer(), nullable=False),
        
        sa.Column('program_year', sa.Integer(), nullable=False),
        sa.Column('semester_no', sa.Integer(), nullable=False),
        sa.Column('semester_name', sa.String(length=50), nullable=False),
        
        # Credit requirements
        sa.Column('total_credits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('min_credits_to_pass', sa.Integer(), nullable=False, server_default='0'),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['regulation_id'], ['regulations.id'], name='fk_regulation_semester_regulation', ondelete='CASCADE'),
        sa.UniqueConstraint('regulation_id', 'semester_no', name='uq_regulation_semester'),
        
        # Check constraints
        sa.CheckConstraint('program_year >= 1 AND program_year <= 5', name='ck_semester_program_year'),
        sa.CheckConstraint('semester_no >= 1 AND semester_no <= 10', name='ck_semester_semester_no'),
        sa.CheckConstraint('total_credits >= 0', name='ck_semester_total_credits'),
        sa.CheckConstraint('min_credits_to_pass >= 0', name='ck_semester_min_credits'),
    )
    
    # Create indexes
    op.create_index('ix_regulation_semesters_regulation_id', 'regulation_semesters', ['regulation_id'])
    
    # Create regulation_promotion_rules table
    op.create_table(
        'regulation_promotion_rules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('regulation_id', sa.Integer(), nullable=False),
        
        sa.Column('from_year', sa.Integer(), nullable=False),
        sa.Column('to_year', sa.Integer(), nullable=False),
        
        sa.Column('min_prev_year_percentage', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('min_current_year_percentage', sa.Integer(), nullable=False, server_default='50'),
        
        sa.Column('additional_rules', sa.Text(), nullable=True),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['regulation_id'], ['regulations.id'], name='fk_regulation_promotion_regulation', ondelete='CASCADE'),
        sa.UniqueConstraint('regulation_id', 'from_year', 'to_year', name='uq_regulation_promotion'),
        
        # Check constraints
        sa.CheckConstraint('from_year >= 1 AND from_year <= 5', name='ck_promotion_from_year'),
        sa.CheckConstraint('to_year >= 1 AND to_year <= 5', name='ck_promotion_to_year'),
        sa.CheckConstraint('to_year > from_year', name='ck_promotion_year_order'),
        sa.CheckConstraint('min_prev_year_percentage >= 0 AND min_prev_year_percentage <= 100', name='ck_promotion_prev_pct'),
        sa.CheckConstraint('min_current_year_percentage >= 0 AND min_current_year_percentage <= 100', name='ck_promotion_curr_pct'),
    )
    
    # Create indexes
    op.create_index('ix_regulation_promotion_rules_regulation_id', 'regulation_promotion_rules', ['regulation_id'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('ix_regulation_promotion_rules_regulation_id', table_name='regulation_promotion_rules')
    op.drop_table('regulation_promotion_rules')
    
    op.drop_index('ix_regulation_semesters_regulation_id', table_name='regulation_semesters')
    op.drop_table('regulation_semesters')
    
    op.drop_index('ix_regulation_subjects_subject_code', table_name='regulation_subjects')
    op.drop_index('ix_regulation_subjects_regulation_id', table_name='regulation_subjects')
    op.drop_table('regulation_subjects')
    
    op.drop_index('ix_regulations_is_active', table_name='regulations')
    op.drop_index('ix_regulations_is_locked', table_name='regulations')
    op.drop_index('ix_regulations_program_id', table_name='regulations')
    op.drop_index('ix_regulations_regulation_code', table_name='regulations')
    op.drop_table('regulations')
