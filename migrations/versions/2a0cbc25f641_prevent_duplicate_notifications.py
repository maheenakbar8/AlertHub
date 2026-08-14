"""prevent duplicate notifications

Revision ID: 2a0cbc25f641
Revises: bbc1e4a37c43
Create Date: 2026-08-14 20:37:35.807488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a0cbc25f641'
down_revision: Union[str, Sequence[str], None] = 'bbc1e4a37c43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("notifications") as batch_op:
        batch_op.create_unique_constraint(
            "uq_user_alert_notification",
            ["user_id", "alert_id"]
        )


def downgrade() -> None:
    with op.batch_alter_table("notifications") as batch_op:
        batch_op.drop_constraint(
            "uq_user_alert_notification",
            type_="unique"
        )