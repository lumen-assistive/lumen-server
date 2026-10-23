"""Tests for device pairing."""

from fastapi.testclient import TestClient


def test_pair_device_returns_a_token(client: TestClient) -> None:
    response = client.post(
        "/api/v1/pairing",
        json={"caregiver_display_name": "Maria", "device_label": "Pixel di Maria"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["device_id"] > 0
    assert body["caregiver_id"] > 0
    assert len(body["token"]) > 20


def test_each_pairing_gets_a_distinct_token(client: TestClient) -> None:
    first = client.post(
        "/api/v1/pairing",
        json={"caregiver_display_name": "Maria", "device_label": "Telefono 1"},
    ).json()
    second = client.post(
        "/api/v1/pairing",
        json={"caregiver_display_name": "Maria", "device_label": "Telefono 2"},
    ).json()

    assert first["token"] != second["token"]
