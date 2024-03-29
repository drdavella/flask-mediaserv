"""empty message

Revision ID: 2f06ee37acb1
Revises: dea34f9c3041
Create Date: 2022-08-09 01:08:45.633698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f06ee37acb1'
down_revision = 'dea34f9c3041'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('album_image',
    sa.Column('width', sa.Integer(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('mimetype', sa.String(length=255), nullable=False),
    sa.Column('original', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['album.id'], ),
    sa.PrimaryKeyConstraint('width', 'height', 'id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('album_image')
    # ### end Alembic commands ###
