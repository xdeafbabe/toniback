"""Create Post table

Revision ID: 19abdec66bac
Revises:
Create Date: 2021-11-18 19:53:39.988985
"""

import alembic
import sqlalchemy


revision = '19abdec66bac'
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
            sqlalchemy.DateTime(),
            server_default=sqlalchemy.text('NOW()'),
            nullable=False,
        ),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime(), nullable=True),
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
