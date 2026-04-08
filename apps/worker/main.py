"""GenUIWar Worker — background job runner entry point."""

import logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the background worker process."""
    logger.info("GenUIWar worker starting (no jobs registered yet)")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
