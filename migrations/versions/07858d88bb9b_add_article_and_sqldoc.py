"""ADD Article and SQLDoc

Revision ID: 07858d88bb9b
Revises: 1880b29828b1
Create Date: 2024-07-16 23:44:58.125173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07858d88bb9b'
down_revision = '1880b29828b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_category',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('parent_id', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['article_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sql_doc_category',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('category', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('article',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('thumbnail', sa.String(length=300), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('like_count', sa.Integer(), nullable=False),
    sa.Column('view_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('category_id', sa.String(length=40), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['article_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sql_doc',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('category_id', sa.String(length=40), nullable=False),
    sa.Column('parent_id', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['sql_doc_category.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['sql_doc.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article_comment',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('nickname', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('like_count', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('article_id', sa.String(length=40), nullable=False),
    sa.Column('parent_id', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['article_comment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article_tags',
    sa.Column('article_id', sa.String(length=40), nullable=False),
    sa.Column('tag_id', sa.String(length=40), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('article_id', 'tag_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article_tags')
    op.drop_table('article_comment')
    op.drop_table('sql_doc')
    op.drop_table('article')
    op.drop_table('tag')
    op.drop_table('sql_doc_category')
    op.drop_table('article_category')
    # ### end Alembic commands ###
