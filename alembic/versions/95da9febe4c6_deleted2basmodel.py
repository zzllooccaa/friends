"""deleted2basmodel

Revision ID: 95da9febe4c6
Revises: a47520af338b
Create Date: 2022-04-23 09:55:54.963792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95da9febe4c6'
down_revision = 'a47520af338b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('like', 'like')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('like', sa.Column('like', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###