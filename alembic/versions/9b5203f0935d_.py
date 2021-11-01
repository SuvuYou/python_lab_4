"""empty message

Revision ID: 9b5203f0935d
Revises: ec85d1ea6ec6
Create Date: 2021-11-02 00:52:48.950640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b5203f0935d'
down_revision = 'ec85d1ea6ec6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('iq', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student', 'iq')
    # ### end Alembic commands ###
