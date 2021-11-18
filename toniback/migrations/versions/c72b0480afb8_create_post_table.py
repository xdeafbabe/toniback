"""Create Post table

Revision ID: c72b0480afb8
Revises:
Create Date: 2021-11-18 21:02:30.713591
"""

import alembic.op
import sqlalchemy


revision = 'c72b0480afb8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    alembic.op.create_table(
        'post',
        sqlalchemy.Column('id', sqlalchemy.Integer(), nullable=False),
        sqlalchemy.Column('title', sqlalchemy.Text(), nullable=False),
        sqlalchemy.Column('content', sqlalchemy.Text(), nullable=False),
        sqlalchemy.Column(
            'created_at',
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.text('NOW()'),
            nullable=False,
        ),
        sqlalchemy.Column(
            'updated_at',
            sqlalchemy.DateTime(timezone=True),
            nullable=True,
        ),
        sqlalchemy.PrimaryKeyConstraint('id'),
    )

    alembic.op.create_index(
        alembic.op.f('ix_post_created_at'),
        'post',
        ['created_at'],
        unique=False,
    )


def downgrade():
    alembic.op.drop_index(
        alembic.op.f('ix_post_created_at'), table_name='post')
    alembic.op.drop_table('post')
