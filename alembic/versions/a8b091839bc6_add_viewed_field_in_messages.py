"""add viewed field in messages

Revision ID: a8b091839bc6
Revises: f37111b3ff73
Create Date: 2019-07-08 15:01:41.073543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8b091839bc6'
down_revision = 'f37111b3ff73'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('messages', sa.Column('viewed', sa.PickleType, default=dict))


def downgrade():
    op.drop_column('messages', 'viewed')
