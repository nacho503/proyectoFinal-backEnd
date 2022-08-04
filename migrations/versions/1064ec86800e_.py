"""empty message

Revision ID: 1064ec86800e
Revises: 2d6c8c1f305b
Create Date: 2022-08-03 00:23:24.984672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1064ec86800e'
down_revision = '2d6c8c1f305b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('I_details_recipe', sa.Column('recipe_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'I_details_recipe', 'recipe', ['recipe_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'I_details_recipe', type_='foreignkey')
    op.drop_column('I_details_recipe', 'recipe_id')
    # ### end Alembic commands ###