"""add_exam_module_tables

Revision ID: f59c2e7cecf3
Revises: 842c524574a4
Create Date: 2025-12-25 13:56:24.593290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f59c2e7cecf3'
down_revision: Union[str, None] = '842c524574a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Create Exam Tables ###
    op.create_table('exam',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('exam_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('academic_year', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('semester_id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False, server_default='DRAFT'),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(['semester_id'], ['semester.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('exam_schedule',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('exam_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('exam_date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('max_marks', sa.Integer(), nullable=False, server_default='100'),
        sa.Column('passing_marks', sa.Integer(), nullable=False, server_default='40'),
        sa.ForeignKeyConstraint(['exam_id'], ['exam.id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('exam_result',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('exam_schedule_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('marks_obtained', sa.Float(), nullable=False),
        sa.Column('grade', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('remarks', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('is_absent', sa.Boolean(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['exam_schedule_id'], ['exam_schedule.id'], ),
        sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('exam_result')
    op.drop_table('exam_schedule')
    op.drop_table('exam')
