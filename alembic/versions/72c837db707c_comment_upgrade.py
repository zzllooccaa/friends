"""comment_upgrade

Revision ID: 72c837db707c
Revises: 1ff06b12ba93
Create Date: 2022-04-23 12:16:55.162123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72c837db707c'
down_revision = '1ff06b12ba93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('numbers_of_likes', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'numbers_of_likes')
    # ### end Alembic commands ###
