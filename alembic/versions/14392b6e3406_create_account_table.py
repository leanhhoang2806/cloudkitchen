"""create account table

Revision ID: 14392b6e3406
Revises: 
Create Date: 2024-04-07 22:26:29.668772

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import CheckConstraint


# revision identifiers, used by Alembic.
revision: str = "14392b6e3406"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the extension if not exists
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create Seller_Info table
    op.create_table(
        "Seller_Info",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("address", sa.String(255), nullable=True),
        sa.Column("zipcode", sa.String(15), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    # Create Buyer_Info table
    op.create_table(
        "Buyer_Info",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("address", sa.String(255), nullable=True),
        sa.Column(
            "seller_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
            server_default=None,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create Dish table
    op.create_table(
        "Dish",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("s3_path", sa.String(255), nullable=True),
        sa.Column("seller_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "is_featured", sa.Boolean(), server_default=sa.text("FALSE"), nullable=True
        ),
        sa.Column("status", sa.String(50), server_default="ACTIVE", nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["seller_id"],
            ["Seller_Info.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create Orders table
    op.create_table(
        "Orders",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("buyer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dish_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("seller_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "quantities",
            sa.Integer,
            CheckConstraint("quantities > 0 AND quantities < 100"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(50),
            server_default="WAITING_FOR_SELLER_CONFIRM",
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["buyer_id"],
            ["Buyer_Info.id"],
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["Dish.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create Purchases table
    op.create_table(
        "Purchases",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dish_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["Dish.id"],
        ),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["Orders.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create Payments table
    op.create_table(
        "Payments",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("picture_upload_limit", sa.Integer(), nullable=False),
        sa.Column("dishes_to_feature_limit", sa.Integer(), nullable=False),
        sa.Column("seller_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["seller_id"],
            ["Seller_Info.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create Featured_dish table
    op.create_table(
        "Featured_dish",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("dish_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["Dish.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create Discounted_Dish table
    op.create_table(
        "Discounted_Dish",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("dish_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("discounted_percentage", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["Dish.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create Chat_Info table
    op.create_table(
        "Chat_Info",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("seller_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("buyer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("conversation_id", sa.String(length=24), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["buyer_id"],
            ["Buyer_Info.id"],
        ),
        sa.ForeignKeyConstraint(
            ["seller_id"],
            ["Seller_Info.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create Dish_Review table
    op.create_table(
        "Dish_Review",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("dish_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("buyer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("content", sa.String(length=255), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("s3_path", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["buyer_id"],
            ["Buyer_Info.id"],
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["Dish.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create Permission table
    op.create_table(
        "Permission",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("user_email", sa.String(length=100), nullable=False),
        sa.Column("permissions", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_email"),
    )


def downgrade():
    op.drop_table("Permission")
    op.drop_table("Dish_Review")
    op.drop_table("Chat_Info")
    op.drop_table("Discounted_Dish")
    op.drop_table("Featured_dish")
    op.drop_table("Payments")
    op.drop_table("Purchases")
    op.drop_table("Orders")
    op.drop_table("Dish")
    op.drop_table("Buyer_Info")
    op.drop_table("Seller_Info")
