"""create complementary_exams tables

Revision ID: aba9c4cfd5ca
Revises: 902acecef906
Create Date: 2024-08-23 13:43:58.975496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aba9c4cfd5ca'
down_revision: Union[str, None] = '902acecef906'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('complementary_exams',
    sa.Column('exam_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('exam_details', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('exam_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('complementary_exams')
    # ### end Alembic commands ###
