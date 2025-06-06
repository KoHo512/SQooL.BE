"""Modify SqlDocCategory

Revision ID: f2fb456c3f72
Revises: 07858d88bb9b
Create Date: 2024-07-20 07:29:15.823577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2fb456c3f72'
down_revision = '07858d88bb9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sql_doc_category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.String(length=40), nullable=True))
        batch_op.create_foreign_key(None, 'sql_doc_category', ['parent_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sql_doc_category', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('parent_id')

    # ### end Alembic commands ###
