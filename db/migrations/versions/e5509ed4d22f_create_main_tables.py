"""create main tables

Revision ID: 12345678654
Revises:
Create Date: 2020-05-05 10:41:35.468471

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '12345678654'
down_revision = None
branch_labels = None
depends_on = None


def create_terms_table() -> None:
    op.create_table(
        'terms',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('iri', sa.Text, nullable=False, unique=True),
        sa.Column('label', sa.Text, nullable=True),
        sa.Column('parent_link', sa.Text, nullable=True),
        sa.Column('mesh_xref', sa.Text, nullable=True)
    )


def create_term_synonyms_table() -> None:
    op.create_table(
        'term_synonyms',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('synonym', sa.Text, nullable=False, unique=True)
    )


def create_term_synonym_relationship_table() -> None:
    op.create_table(
        'term_synonym_relationships',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('term_id', sa.Integer, sa.ForeignKey('terms.id'), nullable=False),
        sa.Column('synonym_id', sa.Integer, sa.ForeignKey('term_synonyms.id'), nullable=False),
        sa.UniqueConstraint('term_id', 'synonym_id', name='term_synonym_relationship')
    )


def upgrade() -> None:
    create_terms_table()
    create_term_synonyms_table()
    create_term_synonym_relationship_table()


def downgrade() -> None:
    op.drop_table('terms')
    op.drop_table('term_synonyms')
    op.drop_table('term_synonym_relationship')
