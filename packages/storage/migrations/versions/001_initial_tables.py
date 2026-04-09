"""Initial tables for calculation results, evidence chunks, and evidence bundles.

Revision ID: 001
Create Date: 2026-04-09
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "calculation_results",
        sa.Column("calculation_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation", sa.String(100), nullable=False),
        sa.Column("inputs", postgresql.JSONB, nullable=False),
        sa.Column("result", postgresql.JSONB, nullable=False),
        sa.Column("trace", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("input_units", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("output_unit", sa.String(50), nullable=True),
        sa.Column("evidence_refs", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "evidence_chunks",
        sa.Column("chunk_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("file_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("content_type", sa.String(50), nullable=False, server_default="text"),
        sa.Column("citation_anchor", postgresql.JSONB, nullable=False),
        sa.Column("metadata", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_evidence_chunks_file_id", "evidence_chunks", ["file_id"])
    op.create_index("ix_evidence_chunks_content_type", "evidence_chunks", ["content_type"])
    op.create_index(
        "ix_evidence_chunks_citation",
        "evidence_chunks",
        ["citation_anchor"],
        postgresql_using="gin",
    )

    op.create_table(
        "evidence_bundles",
        sa.Column("bundle_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("query", sa.Text, nullable=False),
        sa.Column("chunk_ids", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("file_ids", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("total_candidates", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("evidence_bundles")
    op.drop_index("ix_evidence_chunks_citation", table_name="evidence_chunks")
    op.drop_index("ix_evidence_chunks_content_type", table_name="evidence_chunks")
    op.drop_index("ix_evidence_chunks_file_id", table_name="evidence_chunks")
    op.drop_table("evidence_chunks")
    op.drop_table("calculation_results")
