"""create user table

Revision ID: 6a02fba8521c
Revises: 
Create Date: 2023-06-11 20:12:11.939603

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = "6a02fba8521c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    user = op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True, nullable=False),
        sa.Column("password", sa.String, unique=True, nullable=False),
        sa.Column("created_at", sa.DateTime, default=datetime.now()),
    )


def downgrade() -> None:
    op.drop_table("users")
