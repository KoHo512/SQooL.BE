"""add category column in article

Revision ID: 566b2d43b08d
Revises: 03473b0382e8
Create Date: 2024-07-23 12:11:32.399886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '566b2d43b08d'
down_revision = '03473b0382e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=30), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###
