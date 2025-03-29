"""initial version of a db

Revision ID: 3f56f0e39ec4
Revises:
Create Date: 2025-03-30 00:18:50.204803

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3f56f0e39ec4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("surname", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_table(
        "audio_files",
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("filepath", sa.String(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column(
            "uploaded_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
            name=op.f("fk_audio_files_owner_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audio_files")),
    )


def downgrade() -> None:
    op.drop_table("audio_files")
    op.drop_table("users")
