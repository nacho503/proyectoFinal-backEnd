"""empty message

Revision ID: 95c22ebc8418
Revises: 0e2e42966b51
Create Date: 2022-08-01 19:33:22.515539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95c22ebc8418'
down_revision = '0e2e42966b51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('time', sa.String(), nullable=False))
    op.drop_column('recipe', 'step_by_step')
    op.drop_column('recipe', 'image_recipe')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('image_recipe', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('recipe', sa.Column('step_by_step', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
    op.drop_column('recipe', 'time')
    # ### end Alembic commands ###
