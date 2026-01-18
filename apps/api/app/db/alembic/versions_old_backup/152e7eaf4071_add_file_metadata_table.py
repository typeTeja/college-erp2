"""add_file_metadata_table

Revision ID: 152e7eaf4071
Revises: 97c69a66ea17
Create Date: 2026-01-01 20:22:09.297933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '152e7eaf4071'
down_revision: Union[str, None] = '97c69a66ea17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create file_metadata table
    op.create_table(
        'file_metadata',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('file_key', sa.String(length=500), nullable=False),
        sa.Column('bucket_name', sa.String(length=100), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('file_size', sa.BigInteger(), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('checksum', sa.String(length=64), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('module', sa.Enum(
            'ADMISSIONS', 'STUDENTS', 'FACULTY', 'EXAMS', 'LIBRARY', 
            'HOSTEL', 'FEES', 'COMMUNICATION', 'INSTITUTE', 'OTHER',
            name='filemodule'
        ), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=True),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('uploaded_by', sa.Integer(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tags', sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['uploaded_by'], ['user.id'], ),
    )
    
    # Create indexes
    op.create_index('ix_file_metadata_file_key', 'file_metadata', ['file_key'], unique=True)
    op.create_index('ix_file_metadata_module', 'file_metadata', ['module'])
    op.create_index('ix_file_metadata_entity_type', 'file_metadata', ['entity_type'])
    op.create_index('ix_file_metadata_entity_id', 'file_metadata', ['entity_id'])
    op.create_index('ix_file_metadata_uploaded_at', 'file_metadata', ['uploaded_at'])
    
    # Composite index for entity lookups
    op.create_index(
        'ix_file_metadata_entity', 
        'file_metadata', 
        ['entity_type', 'entity_id']
    )


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_file_metadata_entity', table_name='file_metadata')
    op.drop_index('ix_file_metadata_uploaded_at', table_name='file_metadata')
    op.drop_index('ix_file_metadata_entity_id', table_name='file_metadata')
    op.drop_index('ix_file_metadata_entity_type', table_name='file_metadata')
    op.drop_index('ix_file_metadata_module', table_name='file_metadata')
    op.drop_index('ix_file_metadata_file_key', table_name='file_metadata')
    
    # Drop table
    op.drop_table('file_metadata')
