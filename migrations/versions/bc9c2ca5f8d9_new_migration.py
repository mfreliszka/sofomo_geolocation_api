"""New Migration

Revision ID: bc9c2ca5f8d9
Revises: 43f18eb88856
Create Date: 2025-02-17 16:09:21.956850

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bc9c2ca5f8d9"
down_revision: Union[str, None] = "43f18eb88856"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_ipgeolocation_ip", table_name="ipgeolocation")
    op.create_index(op.f("ix_ipgeolocation_ip"), "ipgeolocation", ["ip"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_ipgeolocation_ip"), table_name="ipgeolocation")
    op.create_index("ix_ipgeolocation_ip", "ipgeolocation", ["ip"], unique=False)
    # ### end Alembic commands ###
