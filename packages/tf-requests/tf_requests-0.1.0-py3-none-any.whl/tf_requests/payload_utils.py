#!/usr/bin/env python3

"""
Utility functions for creating and manipulating API request payloads for the Testing Farm.

This module provides a set of functions to construct, validate, and modify the payload data meant
for API requests to the Testing Farm. It ensures that the payload conforms to the expected structure
and contains all the required fields.

Key Functions:
- _validate_payload: Ensure the payload has all required fields set.
- to_json_string: Convert the payload dictionary into a formatted JSON string.
- create_initial_payload: Generate the initial structure of the payload based on provided parameters.
- update_from_path: Dynamically update the payload's data given a specific path and value.
"""


import json
from typing import Any, Dict, Union


def _validate_payload(payload: Dict[str, Any]):
    """
    Ensure the payload contains all required fields.

    Validates the provided payload dictionary to make sure it includes necessary fields for the
    Testing Farm API request.

    Args:
        payload (Dict[str, Any]): The payload to validate.

    Raises:
        ValueError: If any required field is missing or invalid.
    """
    if "api_key" not in payload or not payload["api_key"]:
        raise ValueError("The 'api_key' parameter is required and cannot be an empty string.")
    if "fmf" not in payload["test"] or not payload["test"]["fmf"]:
        raise ValueError("The 'test.fmf' parameter is required and cannot be an empty dict.")
    if "url" not in payload["test"]["fmf"] or not payload["test"]["fmf"]["url"]:
        raise ValueError("The 'test.fmf.url' parameter is required and cannot be an empty string.")
    if not payload["environments"][0]["arch"]:
        raise ValueError("The 'environments[0].arch' parameter is required and cannot be an empty string.")
    if not payload["environments"][0]["os"]["compose"]:
        raise ValueError("The 'environments[0].os.compose' parameter is required and cannot be an empty string.")


def to_json_string(payload: Dict[str, Any]) -> str:
    """
    Convert the payload to a formatted JSON string.

    Args:
        payload (Dict[str, Any]): The payload to be converted.

    Returns:
        str: A JSON-formatted string representation of the payload.
    """
    return json.dumps(payload, indent=2)


def create_initial_payload(
    api_key: str, fmf_url: str, env_arch: str, env_pool: str, env_os_compose: str
) -> Dict[str, Any]:
    """
    Generate the initial structure of the API request payload.

    This function constructs the basic payload structure required for the Testing Farm API
    based on input parameters.

    Args:
        api_key (str): The Testing Farm key for the API call.
        fmf_url (str): The URL for the git repository with the tmt plan.
        env_arch (str): The architecture for the requested machine.
                        Supported values: aarch64, x86_64.
        env_pool (str): The Testing Farm pool from where the machine is selected.
        env_os_compose (str): The Testing Farm compose requested for the tests.

    Returns:
        Dict[str, Any]: A dictionary representing the initial payload structure.
    """
    payload = {
        "api_key": api_key,
        "test": {"fmf": {"url": fmf_url, "ref": "main", "name": ""}},
        "environments": [
            {
                "arch": env_arch,
                "pool": env_pool,
                "os": {"compose": env_os_compose},
                "tmt": {
                    "context": {},
                    "environment": {},
                },
                "variables": {},
                "secrets": {},
            }
        ],
    }
    _validate_payload(payload)
    return payload


def update_from_path(payload: Dict[str, Any], path: str, value: Union[str, Dict]) -> None:
    """
    Update the payload's data based on a specific path.

    Dynamically modify the payload dictionary by specifying a path and the value to set/update.
    The path is represented as a string with "__" as separators, denoting nested keys.

    Args:
        payload (Dict[str, Any]): The payload to be updated.
        path (str): The path indicating where to update the payload.
        value (Union[str, Dict]): The value to set or update in the payload.

    Raises:
        ValueError: If the updated payload is missing any required fields.
    """
    keys = path.split("__")
    new_data = payload
    for i, key in enumerate(keys):
        if i == len(keys) - 1:  # last key in the path
            new_data[key] = value
        else:
            # We only use one environment but the element is a list, so we use the first element of the list
            if key.startswith("environments"):
                new_data = new_data["environments"][0]
            else:
                new_data = new_data.setdefault(key, {})

    _validate_payload(payload)
