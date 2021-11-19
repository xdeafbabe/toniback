"""Create Blog table

Revision ID: 4f1d738431a0
Revises: c72b0480afb8
Create Date: 2021-11-19 20:01:29.411826
"""

import alembic.op
import sqlalchemy


revision = '4f1d738431a0'
down_revision = 'c72b0480afb8'
branch_labels = None
depends_on = None


def upgrade():
    alembic.op.create_table(
        'blog',
        sqlalchemy.Column('id', sqlalchemy.Integer(), nullable=False),
        sqlalchemy.Column('name', sqlalchemy.Text(), nullable=False),
        sqlalchemy.Column('description', sqlalchemy.Text(), nullable=False),
        sqlalchemy.PrimaryKeyConstraint('id'),
    )


def downgrade():
    alembic.op.drop_table('blog')
