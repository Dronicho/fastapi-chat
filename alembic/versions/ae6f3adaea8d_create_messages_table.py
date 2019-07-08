"""create messages table

Revision ID: ae6f3adaea8d
Revises: 828e7c8a4b86
Create Date: 2019-07-08 13:18:11.529643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae6f3adaea8d'
down_revision = '828e7c8a4b86'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('text', sa.String),
        sa.Column('username', sa.String, sa.ForeignKey('users.username')),
        sa.Column('room_name', sa.String, sa.ForeignKey('rooms.name'))
    )


def downgrade():
    op.drop_table('messages')
