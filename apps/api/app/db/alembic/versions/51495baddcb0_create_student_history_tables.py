"""create_student_history_tables

Revision ID: 51495baddcb0
Revises: 9e006e92bde2
Create Date: 2026-01-05 23:03:59.106407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '51495baddcb0'
down_revision: Union[str, None] = '9e006e92bde2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
