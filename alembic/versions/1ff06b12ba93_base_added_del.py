"""base_added_del

Revision ID: 1ff06b12ba93
Revises: a73206a8cb42
Create Date: 2022-04-23 11:05:12.520527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ff06b12ba93'
down_revision = 'a73206a8cb42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('like', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('posts', sa.Column('deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'deleted')
    op.drop_column('like', 'deleted')
    op.drop_column('comments', 'deleted')
    # ### end Alembic commands ###
