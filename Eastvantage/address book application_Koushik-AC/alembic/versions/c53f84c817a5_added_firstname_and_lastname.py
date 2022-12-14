"""Added firstName and lastName

Revision ID: c53f84c817a5
Revises: 286f10c6ec34
Create Date: 2022-08-06 12:47:57.200967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c53f84c817a5'
down_revision = '286f10c6ec34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('firstName', sa.String(length=50), nullable=True))
    op.add_column('account', sa.Column('lastName', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account', 'lastName')
    op.drop_column('account', 'firstName')
    # ### end Alembic commands ###
