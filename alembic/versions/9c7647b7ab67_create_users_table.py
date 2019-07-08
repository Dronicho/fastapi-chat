"""create users table

Revision ID: 9c7647b7ab67
Revises: 
Create Date: 2019-07-08 13:08:44.934126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c7647b7ab67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True),
        sa.Column('email', sa.String),
        sa.Column('hashed_password', sa.String),
        sa.Column('group_list', sa.PickleType)
    )


def downgrade():
    op.drop_table('users')
