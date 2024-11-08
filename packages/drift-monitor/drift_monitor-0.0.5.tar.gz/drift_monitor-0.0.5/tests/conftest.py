"""Root conftest.py file for pytest configuration."""

# pylint: disable=redefined-outer-name

import datetime as dt
import os
import uuid
from unittest import mock

import jwt
from pytest import fixture


@fixture(scope="session")
def endpoint():
    """Return the server URL."""
    return os.environ["DRIFT_MONITOR_URL"]


@fixture(scope="session")
def token(request):
    """Return the server token."""
    if hasattr(request, "param") and request.param:
        return request.param
    now = dt.datetime.now(dt.timezone.utc).timestamp()
    payload = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": now,
        "exp": now + 10000000,
    }
    token = jwt.encode(payload, "some_key", algorithm="HS256")
    return token


@fixture(scope="session", autouse=True)
def token_mock(token):
    """Patch the access token with a MagicMock."""
    with mock.patch("drift_monitor.utils.access_token") as access_token:
        access_token.return_value = token
        yield access_token


@fixture(scope="module")
def request_mock():
    """Patch requests module with MagicMocks."""
    with mock.patch("drift_monitor.utils.requests") as requests:
        yield requests


@fixture(scope="session")
def experiment(request):
    """Return a new experiment."""
    kwds = request.param if hasattr(request, "param") else {}
    return {
        "id": kwds.get("id", f"{uuid.uuid4()}"),
        "created_ad": dt.datetime.now().isoformat(),
        "name": kwds.get("name", "new_experiment"),
        "description": kwds.get("description", "A new experiment."),
        "public": kwds.get("public", False),
        "permissions": kwds.get("permissions", {}),
    }


@fixture(scope="session")
def drift(request):
    """Return a new drift with parameters from request."""
    default_drift = {
        "id": str(uuid.uuid4()),
        "created_at": dt.datetime.now().isoformat(),
        "model": "model_1",
        "job_status": "Running",
        "concept_drift": {},
        "data_drift": {},
    }
    if hasattr(request, "param"):
        default_drift.update(request.param)
    return default_drift
