"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "BESS Analytics Platform" in response.json()["message"]


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_system_status():
    """Test system status endpoint."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "features" in data


def test_get_battery_metrics():
    """Test get battery metrics endpoint."""
    response = client.get("/api/v1/metrics/battery-001")
    assert response.status_code == 200
    data = response.json()
    assert "battery_id" in data
    assert "soh" in data
    assert "health_status" in data
