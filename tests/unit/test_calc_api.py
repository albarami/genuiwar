"""Tests for calculation API endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from apps.api.main import app


@pytest.fixture()
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture()
async def client() -> AsyncClient:
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac  # type: ignore[misc]


class TestCalcAPI:
    async def test_execute_add(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/api/v1/calculations/execute",
            json={"operation": "add", "inputs": {"a": 10, "b": 5}},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["result"] == 15
        assert data["operation"] == "add"
        assert len(data["trace"]) >= 1

    async def test_execute_percentage_change(
        self, client: AsyncClient
    ) -> None:
        resp = await client.post(
            "/api/v1/calculations/execute",
            json={
                "operation": "percentage_change",
                "inputs": {"old": 100, "new": 130},
            },
        )
        assert resp.status_code == 200
        assert resp.json()["result"] == 30.0

    async def test_execute_divide_by_zero(
        self, client: AsyncClient
    ) -> None:
        resp = await client.post(
            "/api/v1/calculations/execute",
            json={"operation": "divide", "inputs": {"a": 10, "b": 0}},
        )
        assert resp.status_code == 422
        assert "Division by zero" in resp.json()["detail"]

    async def test_execute_unknown_operation(
        self, client: AsyncClient
    ) -> None:
        resp = await client.post(
            "/api/v1/calculations/execute",
            json={"operation": "magic", "inputs": {}},
        )
        assert resp.status_code == 422
        assert "Unknown operation" in resp.json()["detail"]

    async def test_execute_invalid_inputs(
        self, client: AsyncClient
    ) -> None:
        resp = await client.post(
            "/api/v1/calculations/execute",
            json={"operation": "add", "inputs": {"a": 10}},
        )
        assert resp.status_code == 422

    async def test_get_calculation_by_id(
        self, client: AsyncClient
    ) -> None:
        exec_resp = await client.post(
            "/api/v1/calculations/execute",
            json={"operation": "add", "inputs": {"a": 1, "b": 2}},
        )
        calc_id = exec_resp.json()["calculation_id"]

        get_resp = await client.get(
            f"/api/v1/calculations/{calc_id}"
        )
        assert get_resp.status_code == 200
        assert get_resp.json()["calculation_id"] == calc_id
        assert get_resp.json()["result"] == 3

    async def test_get_calculation_not_found(
        self, client: AsyncClient
    ) -> None:
        resp = await client.get(
            "/api/v1/calculations/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404
