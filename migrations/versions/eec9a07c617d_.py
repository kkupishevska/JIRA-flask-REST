"""empty message

Revision ID: eec9a07c617d
Revises: f42e89bedb77
Create Date: 2023-12-04 21:36:19.186001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eec9a07c617d'
down_revision = 'f42e89bedb77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('issue', 'status',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Enum('OPEN', 'INPROGRESS', 'DONE', 'TODO', 'INREVIEW', 'UNDERREVIEW', 'APPROVED', 'CANCELLED', 'REJECTED', name='status'),
               existing_nullable=False)
    op.alter_column('issue', 'priority',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Enum('HIGHEST', 'HIGH', 'MEDIUM', 'LOW', 'LOWEST', name='priority'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('issue', 'priority',
               existing_type=sa.Enum('HIGHEST', 'HIGH', 'MEDIUM', 'LOW', 'LOWEST', name='priority'),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    op.alter_column('issue', 'status',
               existing_type=sa.Enum('OPEN', 'INPROGRESS', 'DONE', 'TODO', 'INREVIEW', 'UNDERREVIEW', 'APPROVED', 'CANCELLED', 'REJECTED', name='status'),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###