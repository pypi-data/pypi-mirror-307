#!/usr/bin/env python3

"""
Utility functions for managing and manipulating environment variables within the context of CI/CD pipelines.

This module offers various utilities to extract, segregate, and transform environment variables,
with a focus on those used within CI/CD pipelines. The primary functionalities include segregating
environment variables into different categories, extracting data from specific environment meta variables,
and sanitizing job names.
"""


import json
import logging
import os
import re
from typing import Any, Dict, List, Tuple


def _meta_var_extration(meta_var: str) -> Dict[str, Any]:
    """
    Extract data from a meta variable.

    Given a JSON-like (escaped) string, this function transforms it into a dictionary.

    Args:
        meta_var (str): A JSON-like (escaped) string.

    Returns:
        Dict[str, Any]: Dictionary created from the JSON-like structure.
    """
    meta_dict = json.loads(meta_var)
    return meta_dict


def segregate_env_vars(
    secrets_list: List, variables_list: List
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """
    Segregate environment variables into secrets, variables, and configurations.

    Based on predefined lists and transformations, this function categorizes environment variables
    into secrets, variables, and configurations.

    Args:
        secrets_list (List[str]): List of keys designating secret environment variables.
        variables_list (List[str]): List of keys designating regular environment variables.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
            - secrets_env: Dictionary of secrets.
            - variables_env: Dictionary of regular variables.
            - config_env: Dictionary of configurations.

    Raises:
        ValueError: if any of the 'required_config_keys' is missing from the ENV vars
    """
    # Known transformations
    transformations = {
        "TF_ENDPOINT": "tf_endpoint",
        "TF_API_KEY": "api_key",
        "CI_REPO_URL": "test__fmf__url",
        "CI_REF": "test__fmf__ref",
        "TMT_PLAN": "test__fmf__name",
    }

    secrets_env = {}
    variables_env = {}
    config_env = {}

    # Required keys for building and testing images
    required_images_keys = [
        "ARCH",
        "IMAGE_KEY",
        "TF_COMPOSE",
        "TF_API_KEY",
        "CI_REPO_URL",
    ]

    # Required keys for testing packages
    required_pkgs_keys = [
        "ARCH",
        "TF_API_KEY",
        "WEBSERVER_RELEASES",
    ]

    if os.environ.get("ACTION") == "TEST" and "PACKAGE_NAME" in os.environ:
        required_config_keys = required_pkgs_keys
    else:
        required_config_keys = required_images_keys
    if not all(key in os.environ for key in required_config_keys):
        missing_keys = [key for key in required_config_keys if key not in os.environ]
        raise ValueError(f"Missing keys: {', '.join(missing_keys)}")

    for var, value in os.environ.items():
        # Check if it's a config variable with a known transformation
        if var in transformations:
            config_env[transformations[var]] = value

        # Check if it's a secret
        if var in secrets_list:
            secrets_env[var] = value
        # Check if it's a known variable
        elif var in variables_list:
            variables_env[var] = value
            # Add the variable to the config dict, as some are used in both places
            config_env[var] = value
        # Check for variables passed using a path based variable
        elif var.startswith("environments__variables"):
            # Add it to the config dict, to have it also there.
            # Later will be added properly with update_from_path()
            config_env[var] = value
        # Check for variables passed via META_VARIABLE (a JSON-like string with variables)
        elif var == "META_VARIABLE":
            meta_vars = _meta_var_extration(value)
            variables_env.update(meta_vars)
            # Add it to the config dict, to have it also there.
            config_env.update(meta_vars)
        # Check for variables passed via META_SECRETS (a JSON-like string with secrets)
        elif var == "META_SECRETS":
            meta_secrets = _meta_var_extration(value)
            secrets_env.update(meta_secrets)
        # Check for variables passed via META_CONTEXT (a JSON-like string with tmt context configs)
        elif var == "META_CONTEXT":
            meta_context = _meta_var_extration(value)
            for key in meta_context:
                config_env[f"environments__tmt__context__{key}"] = meta_context[key]
        # Check for variables passed via META_ENVIRONMENT (a JSON-like string with tmt environment configs)
        elif var == "META_ENVIRONMENT":
            meta_environment = _meta_var_extration(value)
            for key in meta_environment:
                config_env[f"environments__tmt__environment__{key}"] = meta_environment[key]
        # Add the rest of EVN variables to the config dict, just in case
        else:
            config_env[var] = value

    # Add the ARCH to a new path based variable, so it can be automatically used later
    config_env["environments__arch"] = config_env["ARCH"]

    logging.debug(f"{config_env=}")
    logging.debug(f"{variables_env=}")
    logging.debug(f"{secrets_env=}")

    return secrets_env, variables_env, config_env


def sanitize_job_name(ci_job_name: str) -> str:
    """
    Sanitize a CI job name.

    Transforms a CI job name by removing specific substrings and replacing certain characters
    to make it more concise and standardized.

    Args:
        ci_job_name (str): The original CI job name.

    Returns:
        str: The sanitized job name.
    """
    # Remove the initial '/plans/' to make it shorter and more meaningful
    job_name = ci_job_name.replace("/plans/", "")
    # Use regular expression to perform transformations
    job_name = re.sub(r"[\s\[\]]", "", job_name)  # Remove spaces, [ and ]
    job_name = re.sub(r"/", "-", job_name)  # Replace / with -
    return job_name
