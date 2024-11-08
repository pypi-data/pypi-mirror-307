"""Test module for creation of drifts."""

from unittest import mock

import pytest

import drift_monitor


@pytest.fixture(scope="function", autouse=True)
def mocks(request_mock, experiment):
    """Mock the requests module."""
    m = mock.MagicMock(json=lambda: experiment)
    request_mock.post.return_value = m


@pytest.fixture(scope="function")
def create_experiment(request_mock, experiment):
    """Create a drift run on the drift monitor server."""
    return drift_monitor.new_experiment(
        name=experiment["name"],
        description=experiment["description"],
        public=experiment["public"],
    )


@pytest.mark.usefixtures("create_experiment")
def test_create_experiment(request_mock, endpoint, token, experiment):
    """Test the drift run was created on the server."""
    assert request_mock.post.call_count == 1
    url = f"{endpoint}/api/v1/experiment"
    assert request_mock.post.call_args[1]["url"] == url
    assert request_mock.post.call_args[1]["headers"] == {
        "Authorization": f"Bearer {token}",
    }
    assert request_mock.post.call_args[1]["json"] == {
        "name": experiment["name"],
        "description": experiment["description"],
        "public": experiment["public"],
        "permissions": experiment["permissions"],
    }
