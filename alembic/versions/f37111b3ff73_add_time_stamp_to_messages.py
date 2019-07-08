"""add time stamp to messages

Revision ID: f37111b3ff73
Revises: ae6f3adaea8d
Create Date: 2019-07-08 13:21:38.238410

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = 'f37111b3ff73'
down_revision = 'ae6f3adaea8d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('messages', sa.Column('timestamp', sa.DateTime, default=datetime.datetime.now))


def downgrade():
    op.drop_column('messages', 'timestamp')
