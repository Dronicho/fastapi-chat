"""create rooms table

Revision ID: 828e7c8a4b86
Revises: 9c7647b7ab67
Create Date: 2019-07-08 13:15:04.259143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '828e7c8a4b86'
down_revision = '9c7647b7ab67'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, unique=True),
        sa.Column('messages', sa.PickleType, default=list)
    )


def downgrade():
    op.drop_table('rooms')
