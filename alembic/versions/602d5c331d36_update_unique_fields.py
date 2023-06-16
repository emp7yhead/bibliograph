"""update unique fields

Revision ID: 602d5c331d36
Revises: 59486c32aa36
Create Date: 2023-06-17 01:20:34.823690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '602d5c331d36'
down_revision = '59486c32aa36'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    # ### end Alembic commands ###
