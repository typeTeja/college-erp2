"""add_staff_management_tables

Revision ID: daa0aa1f2d1b
Revises: 5049f0630fca
Create Date: 2025-12-25 16:18:35.481099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'daa0aa1f2d1b'
down_revision: Union[str, None] = '5049f0630fca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create Shift Table
    op.create_table('shift',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. Create Staff Table
    op.create_table('staff',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('mobile', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('department', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('designation', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('join_date', sa.Date(), nullable=False),
        sa.Column('shift_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['shift_id'], ['shift.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_staff_email'), 'staff', ['email'], unique=True)
    op.create_index(op.f('ix_staff_mobile'), 'staff', ['mobile'], unique=True)

    # 3. Create Maintenance Ticket Table
    op.create_table('maintenanceticket',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('location', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('priority', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('reported_by_id', sa.Integer(), nullable=False),
        sa.Column('assigned_to_id', sa.Integer(), nullable=True),
        
        sa.ForeignKeyConstraint(['reported_by_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['assigned_to_id'], ['staff.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('maintenanceticket')
    op.drop_index(op.f('ix_staff_mobile'), table_name='staff')
    op.drop_index(op.f('ix_staff_email'), table_name='staff')
    op.drop_table('staff')
    op.drop_table('shift')
