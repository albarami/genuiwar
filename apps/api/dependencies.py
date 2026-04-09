"""Shared repository instances for API route dependency injection."""

from packages.storage import (
    InMemoryBundleRepository,
    InMemoryCalculationRepository,
    InMemoryChunkRepository,
)

chunk_repo = InMemoryChunkRepository()
bundle_repo = InMemoryBundleRepository()
calc_repo = InMemoryCalculationRepository()
