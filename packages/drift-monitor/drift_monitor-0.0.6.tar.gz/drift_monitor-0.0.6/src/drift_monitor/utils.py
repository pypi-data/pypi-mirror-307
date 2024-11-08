"""Utility functions for drift monitor."""

import numpy as np
import requests
from drift_monitor.config import access_token, settings


def create_experiment(attributes):
    """Create a new experiment on the drift monitor server."""
    response = requests.post(
        url=f"{settings.monitor_url}/experiment",
        headers={"Authorization": f"Bearer {access_token()}"},
        json=attributes,
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def get_experiment(experiment_name):
    """Get an experiment from the drift monitor server."""
    response = requests.get(
        url=f"{settings.monitor_url}/experiment",
        headers={"Authorization": f"Bearer {access_token()}"},
        json={"name": experiment_name},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()[0] if response.json() else None


def create_drift(experiment, model):
    """Create a drift run on the drift monitor server."""
    exp_route = f"experiment/{experiment['id']}"
    response = requests.post(
        url=f"{settings.monitor_url}/{exp_route}/drift",
        headers={"Authorization": f"Bearer {access_token()}"},
        json={"model": model, "job_status": "Running"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()
    return response.json()


def complete_drift(experiment, drift):
    """Complete a drift run on the drift monitor server."""
    _drift = {k: v for k, v in drift.items() if k not in {"id", "created_at"}}
    exp_route = f"experiment/{experiment['id']}"
    response = requests.put(
        url=f"{settings.monitor_url}/{exp_route}/drift/{drift['id']}",
        headers={"Authorization": f"Bearer {access_token()}"},
        json={**_drift, "job_status": "Completed"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()


def fail_drift(experiment, drift):
    """Fail a drift run on the drift monitor server."""
    _drift = {k: v for k, v in drift.items() if k not in {"id", "created_at"}}
    exp_route = f"experiment/{experiment['id']}"
    response = requests.put(
        url=f"{settings.monitor_url}/{exp_route}/drift/{drift['id']}",
        headers={"Authorization": f"Bearer {access_token()}"},
        json={**_drift, "job_status": "Failed"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()


def register():
    """Registers the token user in the application database."""
    response = requests.post(
        url=f"{settings.monitor_url}/user",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()


def update_email():
    """Update the email of the token user in the application database."""
    response = requests.put(
        url=f"{settings.monitor_url}/user/self",
        headers={"Authorization": f"Bearer {access_token()}"},
        timeout=settings.DRIFT_MONITOR_TIMEOUT,
        verify=not settings.TESTING,
    )
    response.raise_for_status()


def convert_to_serializable(obj):
    """Recursively convert objects to JSON serializable formats."""
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_to_serializable(element) for element in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.generic, np.number)):
        return obj.item()
    return obj
