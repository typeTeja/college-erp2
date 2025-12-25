"""add_timetable_module_tables

Revision ID: 5049f0630fca
Revises: f59c2e7cecf3
Create Date: 2025-12-25 14:33:06.260968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '5049f0630fca'
down_revision: Union[str, None] = 'f59c2e7cecf3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add columns to Faculty
    op.add_column('faculty', sa.Column('designation', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('faculty', sa.Column('max_weekly_hours', sa.Integer(), nullable=False, server_default='20'))
    
    # 2. Create Master Tables
    op.create_table('timeslot',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('classroom',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classroom_room_number'), 'classroom', ['room_number'], unique=True)
    
    op.create_table('timetabletemplate',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # 3. Create Timetable Entry Table
    op.create_table('timetable_entry',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('academic_year_id', sa.Integer(), nullable=False),
        sa.Column('semester_id', sa.Integer(), nullable=False),
        sa.Column('section_id', sa.Integer(), nullable=True),
        sa.Column('day_of_week', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('period_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=True),
        sa.Column('faculty_id', sa.Integer(), nullable=True),
        sa.Column('room_id', sa.Integer(), nullable=True),
        
        sa.ForeignKeyConstraint(['semester_id'], ['semester.id'], ),
        sa.ForeignKeyConstraint(['period_id'], ['timeslot.id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
        sa.ForeignKeyConstraint(['faculty_id'], ['faculty.id'], ),
        sa.ForeignKeyConstraint(['room_id'], ['classroom.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 4. Create Adjustments Table
    op.create_table('classadjustment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timetable_entry_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('original_faculty_id', sa.Integer(), nullable=False),
        sa.Column('substitute_faculty_id', sa.Integer(), nullable=True),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('reason', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('created_at', sa.Date(), nullable=False),
        
        sa.ForeignKeyConstraint(['timetable_entry_id'], ['timetable_entry.id'], ),
        sa.ForeignKeyConstraint(['original_faculty_id'], ['faculty.id'], ),
        sa.ForeignKeyConstraint(['substitute_faculty_id'], ['faculty.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('classadjustment')
    op.drop_table('timetable_entry')
    op.drop_table('timetabletemplate')
    op.drop_index(op.f('ix_classroom_room_number'), table_name='classroom')
    op.drop_table('classroom')
    op.drop_table('timeslot')
    op.drop_column('faculty', 'max_weekly_hours')
    op.drop_column('faculty', 'designation')
