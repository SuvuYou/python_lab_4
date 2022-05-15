"""empty message

Revision ID: 8fd58d7fb982
Revises: e3469326d4d8
Create Date: 2021-11-02 14:22:10.735788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fd58d7fb982'
down_revision = 'e3469326d4d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('professor',
    sa.Column('professor_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.Column('subject', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('professor_id')
    )
    op.create_table('student',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.Column('iq', sa.Integer(), nullable=True),
    sa.Column('GPA', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('student_id')
    )
    op.create_table('course',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('professor_id', sa.Integer(), nullable=True),
    sa.Column('subject', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['professor_id'], ['professor.professor_id'], ),
    sa.PrimaryKeyConstraint('course_id')
    )
    op.create_table('course_student',
    sa.Column('course_student_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.student_id'], ),
    sa.PrimaryKeyConstraint('course_student_id')
    )
    op.create_table('join_request',
    sa.Column('join_request_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.student_id'], ),
    sa.PrimaryKeyConstraint('join_request_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('join_request')
    op.drop_table('course_student')
    op.drop_table('course')
    op.drop_table('student')
    op.drop_table('professor')
    # ### end Alembic commands ###