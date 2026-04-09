"""Tests for file upload API endpoint."""

from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from apps.api.main import app

DOCX_MIME = (
    "application/vnd.openxmlformats-officedocument"
    ".wordprocessingml.document"
)


@pytest.fixture()
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture()
async def client() -> AsyncClient:
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac  # type: ignore[misc]


class TestFileUpload:
    async def test_upload_valid_csv(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        csv_path = fixtures_dir / "clean_data.csv"
        with open(csv_path, "rb") as f:
            resp = await client.post(
                "/api/v1/files/upload",
                files={"file": ("clean_data.csv", f, "text/csv")},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["chunk_count"] >= 1
        assert data["file_document"]["file_type"] == "csv"

    async def test_upload_valid_docx(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        docx_path = fixtures_dir / "clean_report.docx"
        with open(docx_path, "rb") as f:
            resp = await client.post(
                "/api/v1/files/upload",
                files={"file": ("clean_report.docx", f, DOCX_MIME)},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["chunk_count"] > 0

    async def test_upload_rejects_unsupported_type(
        self, client: AsyncClient, tmp_path: Path
    ) -> None:
        bad_file = tmp_path / "notes.txt"
        bad_file.write_text("hello")
        with open(bad_file, "rb") as f:
            resp = await client.post(
                "/api/v1/files/upload",
                files={"file": ("notes.txt", f, "text/plain")},
            )
        assert resp.status_code == 422
        assert "Unsupported file type" in resp.json()["detail"]

    async def test_get_file_metadata_after_upload(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        csv_path = fixtures_dir / "clean_data.csv"
        with open(csv_path, "rb") as f:
            upload_resp = await client.post(
                "/api/v1/files/upload",
                files={"file": ("clean_data.csv", f, "text/csv")},
            )
        file_id = upload_resp.json()["file_document"]["file_id"]

        get_resp = await client.get(f"/api/v1/files/{file_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["file_document"]["file_id"] == file_id

    async def test_get_nonexistent_file_returns_404(
        self, client: AsyncClient
    ) -> None:
        resp = await client.get(
            "/api/v1/files/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404

    async def test_upload_xlsx_populates_sheet_names(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        xlsx_path = fixtures_dir / "clean_budget.xlsx"
        with open(xlsx_path, "rb") as f:
            resp = await client.post(
                "/api/v1/files/upload",
                files={"file": (
                    "clean_budget.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument"
                    ".spreadsheetml.sheet",
                )},
            )
        assert resp.status_code == 200
        doc = resp.json()["file_document"]
        assert doc["sheet_names"] is not None
        assert "Headcount" in doc["sheet_names"]

    async def test_upload_pdf_populates_page_count(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        pdf_path = fixtures_dir / "clean_memo.pdf"
        with open(pdf_path, "rb") as f:
            resp = await client.post(
                "/api/v1/files/upload",
                files={"file": ("clean_memo.pdf", f, "application/pdf")},
            )
        assert resp.status_code == 200
        doc = resp.json()["file_document"]
        assert doc["page_count"] is not None
        assert doc["page_count"] >= 2

    async def test_upload_csv_populates_detected_schema(
        self, client: AsyncClient, fixtures_dir: Path
    ) -> None:
        csv_path = fixtures_dir / "clean_data.csv"
        with open(csv_path, "rb") as f:
            resp = await client.post(
                "/api/v1/files/upload",
                files={"file": ("clean_data.csv", f, "text/csv")},
            )
        assert resp.status_code == 200
        doc = resp.json()["file_document"]
        assert doc["detected_schema"] is not None
        assert "headers" in doc["detected_schema"]
