"""Shared fixtures for unit tests."""

from pathlib import Path

import pytest

FIXTURES_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "packages"
    / "synthetic_data"
    / "fixtures"
)


@pytest.fixture()
def fixtures_dir() -> Path:
    """Return the path to the synthetic fixtures directory."""
    assert FIXTURES_DIR.exists(), (
        f"Fixtures dir missing: {FIXTURES_DIR}. "
        "Run: python -m packages.synthetic_data.generate"
    )
    return FIXTURES_DIR
