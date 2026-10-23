"""Tests for the model pack metadata endpoint."""

from fastapi.testclient import TestClient


def test_model_catalog_starts_empty(client: TestClient) -> None:
    response = client.get("/api/v1/models")

    assert response.status_code == 200
    assert response.json() == []
