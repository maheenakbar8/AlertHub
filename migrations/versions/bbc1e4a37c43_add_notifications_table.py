"""add notifications table

Revision ID: bbc1e4a37c43
Revises: 574171aafa1c
Create Date: 2026-08-13 15:20:03.995136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbc1e4a37c43'
down_revision: Union[str, Sequence[str], None] = '574171aafa1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("alert_id", sa.Integer(), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("notifications")
