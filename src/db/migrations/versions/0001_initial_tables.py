"""initial_tables

Revision ID: 0001
Revises:
Create Date: 2026-06-18 00:00:00.000000
"""


import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "personalities",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False, unique=True),
        sa.Column("system_prompt", sa.Text(), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False, server_default="0.7"),
        sa.Column("max_tokens", sa.Integer(), nullable=False, server_default="2048"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            onupdate=sa.func.now(),
        ),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False, unique=True, index=True),
        sa.Column("username", sa.String(128), nullable=True),
        sa.Column("first_name", sa.String(256), nullable=True),
        sa.Column("language", sa.String(10), nullable=False, server_default="es"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            onupdate=sa.func.now(),
        ),
    )

    op.create_table(
        "chats",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column(
            "telegram_chat_id", sa.BigInteger(), nullable=False, unique=True, index=True
        ),
        sa.Column("chat_type", sa.String(32), nullable=False),
        sa.Column("title", sa.String(512), nullable=True),
        sa.Column("personality_id", sa.String(32), sa.ForeignKey("personalities.id"), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("chat_id", sa.String(32), sa.ForeignKey("chats.id"), nullable=False, index=True),
        sa.Column("user_id", sa.String(32), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("role", sa.String(16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("tokens", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_table(
        "conversations",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("chat_id", sa.String(32), sa.ForeignKey("chats.id"), nullable=False, index=True),
        sa.Column("title", sa.String(512), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_table(
        "memories",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("user_id", sa.String(32), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding_id", sa.String(128), nullable=True, unique=True),
        sa.Column("importance", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_table(
        "documents",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("chat_id", sa.String(32), sa.ForeignKey("chats.id"), nullable=True),
        sa.Column("user_id", sa.String(32), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(512), nullable=False),
        sa.Column("file_path", sa.String(1024), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("documents")
    op.drop_table("memories")
    op.drop_table("conversations")
    op.drop_table("messages")
    op.drop_table("chats")
    op.drop_table("users")
    op.drop_table("personalities")
