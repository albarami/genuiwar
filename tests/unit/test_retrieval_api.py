"""Tests for retrieval API endpoints — upload then retrieve."""

from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from apps.api.main import app
from packages.retrieval.store import chunk_store


@pytest.fixture()
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(autouse=True)
def _clear_store() -> None:
    chunk_store.clear()


@pytest.fixture()
async def client() -> AsyncClient:
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac  # type: ignore[misc]


async def _upload_csv(client: AsyncClient, fixtures_dir: Path) -> str:
    csv_path = fixtures_dir / "clean_data.csv"
    with open(csv_path, "rb") as f:
        resp = await client.post(
            "/api/v1/files/upload",
            files={"file": ("clean_data.csv", f, "text/csv")},
        )
    assert resp.status_code == 200
    return resp.json()["file_document"]["file_id"]


class TestRetrievalAPI:
    async def test_retrieve_after_upload(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        await _upload_csv(client, fixtures_dir)

        resp = await client.post(
            "/api/v1/evidence/retrieve",
            json={"query": "Ahmed"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["chunk_count"] >= 1
        assert data["bundle"]["query"] == "Ahmed"

    async def test_retrieve_no_match(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        await _upload_csv(client, fixtures_dir)

        resp = await client.post(
            "/api/v1/evidence/retrieve",
            json={"query": "nonexistent_xyz_term"},
        )
        assert resp.status_code == 200
        assert resp.json()["chunk_count"] == 0

    async def test_retrieve_empty_query(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        await _upload_csv(client, fixtures_dir)

        resp = await client.post(
            "/api/v1/evidence/retrieve",
            json={"query": ""},
        )
        assert resp.status_code == 200
        assert resp.json()["chunk_count"] == 0

    async def test_get_bundle_by_id(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        await _upload_csv(client, fixtures_dir)

        ret = await client.post(
            "/api/v1/evidence/retrieve",
            json={"query": "Salary"},
        )
        bundle_id = ret.json()["bundle"]["bundle_id"]

        resp = await client.get(f"/api/v1/evidence/bundle/{bundle_id}")
        assert resp.status_code == 200
        assert resp.json()["bundle_id"] == bundle_id

    async def test_get_bundle_not_found(
        self, client: AsyncClient
    ) -> None:
        resp = await client.get(
            "/api/v1/evidence/bundle/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404

    async def test_get_chunks_for_file(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        file_id = await _upload_csv(client, fixtures_dir)

        resp = await client.get(f"/api/v1/evidence/chunks/{file_id}")
        assert resp.status_code == 200
        chunks = resp.json()
        assert len(chunks) >= 1

    async def test_get_chunks_file_not_found(
        self, client: AsyncClient
    ) -> None:
        resp = await client.get(
            "/api/v1/evidence/chunks/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404

    async def test_retrieve_with_top_k(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        await _upload_csv(client, fixtures_dir)

        resp = await client.post(
            "/api/v1/evidence/retrieve",
            json={"query": "Ahmed Sara Khalid", "top_k": 1},
        )
        assert resp.status_code == 200
        assert resp.json()["chunk_count"] <= 1
