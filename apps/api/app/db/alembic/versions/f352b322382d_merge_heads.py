"""merge_heads

Revision ID: f352b322382d
Revises: 51495baddcb0, 7f3a8b9c4d5e
Create Date: 2026-01-05 23:21:09.228617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f352b322382d'
down_revision: Union[str, None] = ('51495baddcb0', '7f3a8b9c4d5e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
