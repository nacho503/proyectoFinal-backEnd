"""empty message

Revision ID: 0249695ed918
Revises: 
Create Date: 2022-07-03 23:07:11.217775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0249695ed918'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingrediente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre_ingrediente', sa.String(length=250), nullable=False),
    sa.Column('calorias', sa.Integer(), nullable=False),
    sa.Column('carbohidratos', sa.Integer(), nullable=False),
    sa.Column('grasa', sa.Integer(), nullable=False),
    sa.Column('proteinas', sa.Integer(), nullable=False),
    sa.Column('categoria', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.Column('mail', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('despensa',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('id_ingrediente', sa.Integer(), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ingrediente'], ['ingrediente.id'], ),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('id_ingrediente', sa.Integer(), nullable=False),
    sa.Column('nombre_receta', sa.String(length=250), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(timezone=250), nullable=False),
    sa.Column('paso_a_paso', sa.String(length=250), nullable=False),
    sa.ForeignKeyConstraint(['id_ingrediente'], ['ingrediente.id'], ),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comentario__valor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('id_receta', sa.Integer(), nullable=False),
    sa.Column('comentario', sa.String(length=250), nullable=False),
    sa.Column('valoracion', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_receta'], ['receta.id'], ),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorito',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('id_receta', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_receta'], ['receta.id'], ),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorito')
    op.drop_table('comentario__valor')
    op.drop_table('receta')
    op.drop_table('despensa')
    op.drop_table('usuario')
    op.drop_table('ingrediente')
    # ### end Alembic commands ###
