"""

Revision ID: 781c495db04e
Revises: 78b953d7f5a3
Create Date: 2018-08-13 07:26:26.973977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '781c495db04e'
down_revision = '78b953d7f5a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('spam_model', sa.Column('classifier', sa.String(length=50), nullable=True))
    op.create_index(op.f('ix_spam_model_classifier'), 'spam_model', ['classifier'], unique=False)
    op.create_index(op.f('ix_spam_model_status'), 'spam_model', ['status'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_spam_model_status'), table_name='spam_model')
    op.drop_index(op.f('ix_spam_model_classifier'), table_name='spam_model')
    op.drop_column('spam_model', 'classifier')
    # ### end Alembic commands ###
