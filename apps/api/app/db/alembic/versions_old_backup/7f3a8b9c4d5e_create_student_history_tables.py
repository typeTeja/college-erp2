"""create_student_history_tables

Revision ID: 7f3a8b9c4d5e
Revises: 9e006e92bde2
Create Date: 2026-01-05 23:04:00

Creates student history tables:
- student_semester_history (with merged credit tracking)
- student_promotion_logs
- student_regulation_migrations

NOTE: StudentCreditTracker has been REMOVED (merged into student_semester_history)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f3a8b9c4d5e'
down_revision: Union[str, None] = '9e006e92bde2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create student_semester_history table (SINGLE SOURCE OF TRUTH)
    op.create_table(
        'student_semester_history',
        sa.Column('id', sa.Integer(), nullable=False),
        
        # Student links
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('academic_year_id', sa.Integer(), nullable=False),
        sa.Column('regulation_id', sa.Integer(), nullable=False),
        
        # Semester identification
        sa.Column('program_year', sa.Integer(), nullable=False),
        sa.Column('semester_no', sa.Integer(), nullable=False),
        
        # CREDIT TRACKING (merged from StudentCreditTracker)
        sa.Column('total_credits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('earned_credits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('failed_credits', sa.Integer(), nullable=False, server_default='0'),
        
        # Status
        sa.Column('status', sa.String(length=20), nullable=False),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='fk_semester_history_student'),
        sa.ForeignKeyConstraint(['batch_id'], ['academic_batches.id'], name='fk_semester_history_batch'),
        sa.ForeignKeyConstraint(['academic_year_id'], ['academic_year.id'], name='fk_semester_history_academic_year'),
        sa.ForeignKeyConstraint(['regulation_id'], ['regulations.id'], name='fk_semester_history_regulation'),
        sa.UniqueConstraint('student_id', 'academic_year_id', 'semester_no', name='uq_student_semester'),
        
        # Check constraints
        sa.CheckConstraint('program_year >= 1 AND program_year <= 5', name='ck_semester_history_program_year'),
        sa.CheckConstraint('semester_no >= 1 AND semester_no <= 10', name='ck_semester_history_semester_no'),
        sa.CheckConstraint('total_credits >= 0', name='ck_semester_history_total_credits'),
        sa.CheckConstraint('earned_credits >= 0', name='ck_semester_history_earned_credits'),
        sa.CheckConstraint('failed_credits >= 0', name='ck_semester_history_failed_credits'),
    )
    
    # Create indexes
    op.create_index('ix_student_semester_history_student_id', 'student_semester_history', ['student_id'])
    op.create_index('ix_student_semester_history_batch_id', 'student_semester_history', ['batch_id'])
    op.create_index('ix_student_semester_history_academic_year_id', 'student_semester_history', ['academic_year_id'])
    
    # Create student_promotion_logs table
    op.create_table(
        'student_promotion_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('regulation_id', sa.Integer(), nullable=False),
        
        # Promotion details
        sa.Column('from_year', sa.Integer(), nullable=False),
        sa.Column('to_year', sa.Integer(), nullable=False),
        sa.Column('from_semester', sa.Integer(), nullable=False),
        sa.Column('to_semester', sa.Integer(), nullable=False),
        
        # Decision
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        
        # Credits summary
        sa.Column('year_total_credits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('year_earned_credits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('year_failed_credits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('year_percentage', sa.DECIMAL(5, 2), nullable=True),
        
        # Decision maker
        sa.Column('decided_by', sa.Integer(), nullable=False),
        sa.Column('decided_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='fk_promotion_log_student'),
        sa.ForeignKeyConstraint(['batch_id'], ['academic_batches.id'], name='fk_promotion_log_batch'),
        sa.ForeignKeyConstraint(['regulation_id'], ['regulations.id'], name='fk_promotion_log_regulation'),
        sa.ForeignKeyConstraint(['decided_by'], ['user.id'], name='fk_promotion_log_decided_by'),
        
        # Check constraints
        sa.CheckConstraint('from_year >= 1 AND from_year <= 5', name='ck_promotion_log_from_year'),
        sa.CheckConstraint('to_year >= 1 AND to_year <= 5', name='ck_promotion_log_to_year'),
        sa.CheckConstraint('from_semester >= 1 AND from_semester <= 10', name='ck_promotion_log_from_semester'),
        sa.CheckConstraint('to_semester >= 1 AND to_semester <= 10', name='ck_promotion_log_to_semester'),
        sa.CheckConstraint('year_total_credits >= 0', name='ck_promotion_log_total_credits'),
        sa.CheckConstraint('year_earned_credits >= 0', name='ck_promotion_log_earned_credits'),
        sa.CheckConstraint('year_failed_credits >= 0', name='ck_promotion_log_failed_credits'),
    )
    
    # Create indexes
    op.create_index('ix_student_promotion_logs_student_id', 'student_promotion_logs', ['student_id'])
    op.create_index('ix_student_promotion_logs_batch_id', 'student_promotion_logs', ['batch_id'])
    
    # Create student_regulation_migrations table
    op.create_table(
        'student_regulation_migrations',
        sa.Column('id', sa.Integer(), nullable=False),
        
        sa.Column('student_id', sa.Integer(), nullable=False),
        
        # Migration details
        sa.Column('from_regulation_id', sa.Integer(), nullable=False),
        sa.Column('to_regulation_id', sa.Integer(), nullable=False),
        
        sa.Column('migration_date', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('reason', sa.Text(), nullable=False),
        
        # Approval
        sa.Column('approved_by', sa.Integer(), nullable=False),
        sa.Column('approved_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='fk_regulation_migration_student'),
        sa.ForeignKeyConstraint(['from_regulation_id'], ['regulations.id'], name='fk_regulation_migration_from'),
        sa.ForeignKeyConstraint(['to_regulation_id'], ['regulations.id'], name='fk_regulation_migration_to'),
        sa.ForeignKeyConstraint(['approved_by'], ['user.id'], name='fk_regulation_migration_approved_by'),
    )
    
    # Create indexes
    op.create_index('ix_student_regulation_migrations_student_id', 'student_regulation_migrations', ['student_id'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('ix_student_regulation_migrations_student_id', table_name='student_regulation_migrations')
    op.drop_table('student_regulation_migrations')
    
    op.drop_index('ix_student_promotion_logs_batch_id', table_name='student_promotion_logs')
    op.drop_index('ix_student_promotion_logs_student_id', table_name='student_promotion_logs')
    op.drop_table('student_promotion_logs')
    
    op.drop_index('ix_student_semester_history_academic_year_id', table_name='student_semester_history')
    op.drop_index('ix_student_semester_history_batch_id', table_name='student_semester_history')
    op.drop_index('ix_student_semester_history_student_id', table_name='student_semester_history')
    op.drop_table('student_semester_history')
