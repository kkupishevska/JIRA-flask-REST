"""empty message

Revision ID: f42e89bedb77
Revises: ec710ddb042d
Create Date: 2023-12-01 15:16:03.002495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f42e89bedb77'
down_revision = 'ec710ddb042d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('ownerId', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'project', 'user', ['ownerId'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='foreignkey')
    op.drop_column('project', 'ownerId')
    # ### end Alembic commands ###
