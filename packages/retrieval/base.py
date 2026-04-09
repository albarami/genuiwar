"""Retrieval contract: base class and filter model."""

from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from packages.schemas.evidence import EvidenceBundle


class RetrievalFilters(BaseModel):
    """Optional filters to narrow retrieval scope."""

    file_ids: list[UUID] | None = None
    content_type: str | None = None
    sheet_name: str | None = None


class BaseRetriever(ABC):
    """Abstract contract for evidence retrieval backends."""

    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int,
        filters: RetrievalFilters | None = None,
    ) -> EvidenceBundle:
        """Retrieve the most relevant evidence chunks for a query.

        Args:
            query: The natural-language question or search terms.
            top_k: Maximum number of chunks to return.
            filters: Optional filters to narrow scope.

        Returns:
            EvidenceBundle with ranked chunks, citation anchors preserved.
        """
