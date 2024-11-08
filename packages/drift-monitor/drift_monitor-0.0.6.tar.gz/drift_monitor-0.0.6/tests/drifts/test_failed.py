"""Test module for creation of experiments."""

from unittest import mock

import pytest

from drift_monitor import DriftMonitor


@pytest.fixture(scope="module", autouse=True)
def mocks(request_mock, experiment, drift):
    """Mock the requests module."""
    m = mock.MagicMock(json=lambda: [experiment.copy()])
    request_mock.get.return_value = m
    m = mock.MagicMock(json=lambda: drift.copy())
    request_mock.post.return_value = m


@pytest.fixture(scope="module")
def create_drift(request_mock, experiment, drift):
    """Create a drift run on the drift monitor server."""
    try:
        with DriftMonitor(experiment["name"], drift["model"]):
            raise ValueError("Failed to create drift run.")
    except ValueError:
        pass


@pytest.mark.usefixtures("create_drift")
def test_running_drift(request_mock, endpoint, experiment, token):
    """Test the drift run was created on the server."""
    assert request_mock.post.call_count == 1
    url = f"{endpoint}/api/v1/experiment/{experiment['id']}/drift"
    assert request_mock.post.call_args[1]["url"] == url
    assert request_mock.post.call_args[1]["headers"] == {
        "Authorization": f"Bearer {token}",
    }
    json = request_mock.post.call_args[1]["json"]
    assert json["job_status"] == "Running"
    assert "concept_drift" not in json
    assert "data_drift" not in json


@pytest.mark.usefixtures("create_drift")
def test_completed_drift(request_mock, endpoint, experiment, token, drift):
    """Test the drift run was completed on the server."""
    assert request_mock.put.call_count == 1
    url = f"{endpoint}/api/v1/experiment/{experiment['id']}"
    url += f"/drift/{drift['id']}"
    assert request_mock.put.call_args[1]["url"] == url
    assert request_mock.put.call_args[1]["headers"] == {
        "Authorization": f"Bearer {token}",
    }
    json = request_mock.put.call_args[1]["json"]
    assert json["job_status"] == "Failed"
    assert json["concept_drift"] == {}
    assert json["data_drift"] == {}
