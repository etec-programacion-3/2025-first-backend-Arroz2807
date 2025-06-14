"""Crear tabla libros

Revision ID: 715bd01bca6a
Revises: 
Create Date: 2025-04-23 11:15:39.343854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '715bd01bca6a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('libros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=255), nullable=False),
    sa.Column('autor', sa.String(length=255), nullable=False),
    sa.Column('isbn', sa.String(length=13), nullable=False),
    sa.Column('categoria', sa.String(length=100), nullable=False),
    sa.Column('estado', sa.String(length=50), nullable=True),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('isbn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('libros')
    # ### end Alembic commands ###
