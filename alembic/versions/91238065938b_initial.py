"""initial

Revision ID: 91238065938b
Revises: 
Create Date: 2024-02-16 14:18:17.170420

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "91238065938b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "waze",
        sa.Column("waze", sa.Text, primary_key=True),
        sa.Column(
            "timestamp_utc",
            sa.DateTime,
            server_default=sa.text("CURRENT_TIMESTAMP NOT NULL"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("waze")
