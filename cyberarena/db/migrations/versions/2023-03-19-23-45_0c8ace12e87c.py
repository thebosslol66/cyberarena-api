"""empty message

Revision ID: 0c8ace12e87c
Revises: 3347a7965430
Create Date: 2023-03-19 23:45:32.168587

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0c8ace12e87c"
down_revision = "3347a7965430"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_model",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=200), nullable=False),
        sa.Column("_password_hash", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("refresh_token_value", sa.String(length=128), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("coins", sa.BigInteger(), nullable=False),
        sa.Column("last_daily_reward", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_model")
    # ### end Alembic commands ###