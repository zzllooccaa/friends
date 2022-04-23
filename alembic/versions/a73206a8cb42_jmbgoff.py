"""jmbgoff

Revision ID: a73206a8cb42
Revises: 95da9febe4c6
Create Date: 2022-04-23 10:00:03.461956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a73206a8cb42'
down_revision = '95da9febe4c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_jmbg_key', 'user', type_='unique')
    op.drop_column('user', 'jmbg')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('jmbg', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_unique_constraint('user_jmbg_key', 'user', ['jmbg'])
    # ### end Alembic commands ###
