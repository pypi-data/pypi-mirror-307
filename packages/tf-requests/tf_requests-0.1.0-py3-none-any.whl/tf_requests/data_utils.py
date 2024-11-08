#!/usr/bin/env python3


"""
Utility functions for manipulating and generating data structures required for Testing Farm API
requests.

This module provides a collection of functions for data extraction, transformation, and generation
tailored for the Testing Farm API. It handles operations such as constructing URLs, determining
compose values, and populating specific board variables based on given parameters.
"""


import json
import logging
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import requests

from .request_utils import HEADER_NO_CACHE


def determine_board_base_url(
    release_name: Optional[str],
    webserver_workspaces: str,
    workspace_id: str,
    s3_upload_prefix: str,
    image_key: str,
    webserver_releases: str,
) -> str:
    """
    Construct the base URL based on the presence or absence of release_name.

    Given a set of parameters, this function generates the appropriate base URL for either
    the pipelines-as-code pipeline or the package-level-pipeline.

    Args:
        release_name (Optional[str]): Name of the release. If None, it indicates the
                                      pipelines-as-code pipeline scenario.
        webserver_workspaces (str): Base URL for webserver workspaces.
        workspace_id (str): ID of the workspace.
        s3_upload_prefix (str): Prefix for S3 upload path.
        image_key (str): Key for the image.
        webserver_releases (str): Base URL for webserver releases.

    Returns:
        str: Constructed base URL.
    """
    if release_name is None:
        # Use by the pipelines-as-code pipeline
        base_url = f"{webserver_workspaces}/{workspace_id}/{s3_upload_prefix}/{image_key}"
    else:
        # Use by the package-level-pipeline. The IMAGE_KEY comes already with the .boot
        base_url = f"{webserver_releases}/{release_name}/{s3_upload_prefix}/{image_key}"

    return base_url


def generate_board_compose(base_url: str, hw_target: str) -> str:
    """
    Generate a JSON (escaped) string with the structure related to a specific board

    E.g.: The JSON structure for RideSX4 would look like this:
    {
        "boot_image": "http://example.com/aboot.img.xz",
        "boot_checksum": "http://example.com/aboot.img.xz.sha256",
        "root_image": "http://example.com/rootfs.simg.xz",
        "root_checksum": "http://example.com/rootfs.simg.xz.sha256",
    }

    The expected output from this function for that structure should look like this:
    "{\"boot_image\": \"http://example.com/aboot.simg.xz\", \"boot_checksum\": \"http://example.com/aboot.simg.xz.sha256\", \"root_image\": \"http://example.com/rootfs.simg.xz\", \"root_checksum\": \"http://example.com/rootfs.simg.xz.sha256\"}" # noqa: E501

    Args:
        base_url (str): Base URL to use in the structure.
        hw_target (str): The code name for the board to be flashed.

    Returns:
        str: A JSON (escaped) string representation of the special board TF composes.
    """
    if base_url:
        if hw_target == "rcar_s4":
            disk_img = f"{base_url}.raw.xz"
            structure = {
                "disk_image": disk_img,
                "disk_checksum": f"{disk_img}.sha256",
            }
        else:
            if not base_url.endswith(".aboot"):
                base_url += ".aboot"
            boot_img = f"{base_url}/aboot.img.xz"
            root_img = f"{base_url}/rootfs.simg.xz"

            structure = {
                "boot_image": boot_img,
                "boot_checksum": f"{boot_img}.sha256",
                "root_image": root_img,
                "root_checksum": f"{root_img}.sha256",
            }
        return json.dumps(structure)
    return json.dumps({})


def determine_tf_compose(
    tf_compose: str,
    action: str,
    image_key: str,
    arch: str,
    stream: str,
    build_format: str,
) -> str:
    """
    Construct the value based on provided arguments.

    Given a set of parameters, this function determines the appropriate compose value for the Testing Farm.

    NOTE: In Testing Farm the aarch64 composes have the '-aarch64' appended to the end.

    Args:
        tf_compose (str): Original defined compose for Testing Farm (e.g., "centos-stream9").
        action (str): Action to be performed. Its value could be either TEST or BUILD.
        image_key (str): Key for the image.
        arch (str): Architecture type (e.g., "aarch64").
        stream (str): Stream type (e.g., "upstream").
        build_format (str): Build format type (e.g., "aboot").

    Returns:
        str: Composed value based on the provided arguments.
    """
    final_tf_compose = tf_compose
    if action == "BUILD" and arch == "aarch64" and stream == "UPSTREAM":
        final_tf_compose = f"{tf_compose}-aarch64"

    if action == "TEST" and "aboot" not in build_format:
        final_tf_compose = image_key

    logging.debug(f"Testing Farm Compose: {final_tf_compose}")

    return final_tf_compose


def populate_board_variables(s3_upload_prefix: str, tf_pool: str, arch: str, hw_target: str) -> Tuple[str, str]:
    """
    Convert the shell function to Python.

    This function populates the appropriate values for 's3_upload' and 'tf_pool' based on
    the provided 'hw_target' and 'arch'.

    Args:
        s3_upload_prefix (str): Initial prefix for S3 upload.
        tf_pool (str): Initial Testing Farm pool value.
        arch (str): Architecture type (e.g., "aarch64").
        hw_target (str): Hardware target type (e.g., "qdrive3").

    Returns:
        Tuple[str, str]: Updated values for 's3_upload_prefix' and 'tf_pool'.
    """
    # FIXME: Maybe put defaults and reorder the parameters

    if hw_target == "qdrive3":
        s3_upload_prefix = "QDrive3"
        if arch == "aarch64":
            tf_pool = "qdrive3-atc"
    elif hw_target == "ridesx4":
        s3_upload_prefix = "RideSX4"
        if arch == "aarch64":
            tf_pool = "ride4-atc"
    elif hw_target == "ti-j784s4":
        s3_upload_prefix = "TI"
        if arch == "aarch64":
            tf_pool = "ti-j784s4-atc"
    elif hw_target == "ti-am69sk":
        s3_upload_prefix = "TI"
        if arch == "aarch64":
            tf_pool = "ti-am69sk-atc"
    elif hw_target == "rcar_s4":
        s3_upload_prefix = "Renesas"
        if arch == "aarch64":
            tf_pool = "rcar-s4-atc"
    else:
        logging.error(f"Not supported board ({hw_target}).")
        sys.exit(2)

    logging.debug(f"Using 's3_upload_prefix={s3_upload_prefix}' and 'tf_pool={tf_pool}")

    return s3_upload_prefix, tf_pool


def find_repo_paths(data: Dict[str, Any]) -> List:
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                result = find_repo_paths(value)
                if result:
                    return result
            elif key == "RPMs" and isinstance(value, list):
                return value
    return []


def get_package_nvr(config: Dict[str, Any], package_name: str) -> str:
    """
    Extracts the Name-Version-Release (NVR) identifier for a specified package from the CAT manifest.

    The CAT manifest is a JSON document containing information about available software packages.
    This function searches for the specified package within the manifest and retrieves its NVR.

    Args:
        config (Dict[str, Any]): Configuration variables used in various operations of the program.
                                It should include keys like 'release_name' and 'webserver_releases'.
        package_name (str): The name of the package for which the NVR is required.

    Returns:
        str: The NVR (Name-Version-Release) string for the specified package.

    Raises:
        Exception: If the CAT manifest cannot be retrieved from any of the defined URLs.
        ValueError: If the response from the server is not a valid JSON or if the specified package
                    is not found in the manifest.
    """
    package_nvr = None
    release_name = config["release_name"]
    base_url = f"{config['webserver_releases']}/{release_name}"

    cat_manifest_paths = [
        "cat-manifests/manifest-source.json",  # The current path
        "cat-manifest/manifest.json",  # The old path
    ]

    response = None
    for path in cat_manifest_paths:
        try:
            url = f"{base_url}/{path}"
            logging.debug(f"CAT manifest URL used: {url}")
            response = requests.get(url, headers=HEADER_NO_CACHE)
            response.raise_for_status()
            cat_manifest_path = path
            break
        except requests.RequestException:
            continue

    if not response:
        logging.info(f"CAT manifest URL used: {url}")
        raise Exception("ERROR: The CAT manifest was not found.")

    logging.info(f"CAT manifest path used for the release {release_name}: '{cat_manifest_path}'")

    try:
        manifest = response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"ERROR: The CAT manifest is not a valid JSON: {e}")

    try:
        rpms = find_repo_paths(manifest)
    except KeyError as e:
        raise ValueError(f"ERROR: The CAT manifest doesn't have the right path for the rpms: {e}")

    # Make sure characters like '+' are properly escaped from the package name
    # This is necessary for packages like 'memtest86+' or 'libsigc++20'
    escaped_package_name = re.escape(package_name)

    # Regular expression to match the pattern: package_name-version-release
    pattern = re.compile(rf"^{escaped_package_name}-\d+(?:\.\d+)*-\d+(?:\.\w+)*")
    for rpm in rpms:
        match = pattern.match(rpm)
        if match:
            # Splitting the matched string to exclude architecture and file extension
            package_nvr = match.group().rsplit(".", 2)[0]

    if not package_nvr:
        raise ValueError(f"ERROR: No NVR was found for the package {package_name}")

    return package_nvr
