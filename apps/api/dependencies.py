"""Repository instances for API route dependency injection.

Selects between in-memory (default) and Postgres backends based on config.
To use Postgres: set RETRIEVAL_BACKEND=postgres in .env and ensure the
database is running with migrations applied.
"""

import structlog

from packages.shared.config import get_settings
from packages.storage import (
    InMemoryBundleRepository,
    InMemoryCalculationRepository,
    InMemoryChunkRepository,
)
from packages.storage.base import (
    BundleRepository,
    CalculationRepository,
    ChunkRepository,
)

logger = structlog.get_logger(__name__)

_settings = get_settings()


def _build_repositories() -> (
    tuple[ChunkRepository, BundleRepository, CalculationRepository]
):
    """Build repository instances based on current config."""
    backend = _settings.retrieval_backend

    if backend == "postgres":
        from packages.storage.database import get_session_factory
        from packages.storage.postgres import (
            PostgresBundleRepository,
            PostgresCalculationRepository,
            PostgresChunkRepository,
        )

        sf = get_session_factory()
        chunk = PostgresChunkRepository(sf)
        calc = PostgresCalculationRepository(sf)
        bundle = PostgresBundleRepository(sf, chunk)
        logger.info("storage_backend", backend="postgres")
        return chunk, bundle, calc

    chunk_mem = InMemoryChunkRepository()
    bundle_mem = InMemoryBundleRepository()
    calc_mem = InMemoryCalculationRepository()
    logger.info("storage_backend", backend="memory")
    return chunk_mem, bundle_mem, calc_mem


chunk_repo, bundle_repo, calc_repo = _build_repositories()
