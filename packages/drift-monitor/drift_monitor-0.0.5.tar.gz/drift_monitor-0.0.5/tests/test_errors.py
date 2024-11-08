"""Test example module."""

import pytest

from drift_monitor import DriftMonitor


@pytest.fixture(scope="function")
def monitor(request_mock, experiment, drift):
    """Create a drift run on the drift monitor server."""
    return DriftMonitor(experiment["name"], drift["model"])


def test_concept_context(monitor):
    """Test the method concept raises out of context error."""
    with pytest.raises(RuntimeError) as excinfo:
        monitor.concept(True, {"threshold": 0.5})
    assert str(excinfo.value) == "Drift monitor context not started."


def test_data_context(monitor):
    """Test the method concept raises out of context error."""
    with pytest.raises(RuntimeError) as excinfo:
        monitor.data(True, {"threshold": 0.5})
    assert str(excinfo.value) == "Drift monitor context not started."
