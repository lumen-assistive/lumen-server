"""Tests for encrypted blob upload and retrieval."""

import base64

from fastapi.testclient import TestClient


def _pair(client: TestClient) -> str:
    response = client.post(
        "/api/v1/pairing",
        json={"caregiver_display_name": "Luca", "device_label": "Tablet di Luca"},
    )
    token: str = response.json()["token"]
    return token


def test_upload_and_fetch_blob_round_trip(client: TestClient) -> None:
    token = _pair(client)
    headers = {"Authorization": f"Bearer {token}"}
    ciphertext = base64.b64encode(b"not-real-plaintext").decode("ascii")

    upload = client.post(
        "/api/v1/blobs",
        json={"category": "daily-status", "ciphertext_base64": ciphertext},
        headers=headers,
    )
    assert upload.status_code == 200
    assert upload.json()["ciphertext_base64"] == ciphertext

    listing = client.get("/api/v1/blobs", headers=headers, params={"category": "daily-status"})
    assert listing.status_code == 200
    categories = [blob["category"] for blob in listing.json()]
    assert categories == ["daily-status"]


def test_upload_without_a_token_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/v1/blobs",
        json={"category": "daily-status", "ciphertext_base64": "AAAA"},
    )

    assert response.status_code == 401


def test_upload_with_an_unknown_token_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/v1/blobs",
        json={"category": "daily-status", "ciphertext_base64": "AAAA"},
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401


def test_upload_with_invalid_base64_is_rejected(client: TestClient) -> None:
    token = _pair(client)

    response = client.post(
        "/api/v1/blobs",
        json={"category": "daily-status", "ciphertext_base64": "not base64!!"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400


def test_a_device_cannot_see_another_devices_blobs(client: TestClient) -> None:
    token_a = _pair(client)
    token_b = _pair(client)

    client.post(
        "/api/v1/blobs",
        json={"category": "daily-status", "ciphertext_base64": "AAAA"},
        headers={"Authorization": f"Bearer {token_a}"},
    )

    listing = client.get("/api/v1/blobs", headers={"Authorization": f"Bearer {token_b}"})

    assert listing.json() == []
