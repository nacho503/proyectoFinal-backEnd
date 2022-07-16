"""empty message

Revision ID: 2d9b9bac3209
Revises: acd0dfea1233
Create Date: 2022-07-15 17:39:56.429610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d9b9bac3209'
down_revision = 'acd0dfea1233'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ingrediente', sa.Column('ingredient_name', sa.String(length=50), nullable=False))
    op.add_column('ingrediente', sa.Column('ingredient_portion', sa.String(length=20), nullable=False))
    op.create_unique_constraint(None, 'ingrediente', ['ingredient_name'])
    op.drop_column('ingrediente', 'grasa')
    op.drop_column('ingrediente', 'proteinas')
    op.drop_column('ingrediente', 'categoria')
    op.drop_column('ingrediente', 'nombre_ingrediente')
    op.drop_column('ingrediente', 'calorias')
    op.drop_column('ingrediente', 'carbohidratos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ingrediente', sa.Column('carbohidratos', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('ingrediente', sa.Column('calorias', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('ingrediente', sa.Column('nombre_ingrediente', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
    op.add_column('ingrediente', sa.Column('categoria', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
    op.add_column('ingrediente', sa.Column('proteinas', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('ingrediente', sa.Column('grasa', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'ingrediente', type_='unique')
    op.drop_column('ingrediente', 'ingredient_portion')
    op.drop_column('ingrediente', 'ingredient_name')
    # ### end Alembic commands ###