"""empty message

Revision ID: c4ef08b4f1ae
Revises: 0f3357cc5e52
Create Date: 2022-07-29 01:15:28.133974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4ef08b4f1ae'
down_revision = '0f3357cc5e52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.String(), nullable=False),
    sa.Column('directory', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scan')
    # ### end Alembic commands ###
