#!/usr/bin/env python3


"""
get_auto_compose command will fetch information about an specific automotive image available
for doing automated test in Testing Farm and it'll return the string with a valid Testing Farm
compose for it.

it fetchs the information from a file like this one:
https://autosd.sig.centos.org/AutoSD-9/nightly/sample-images/AMI_info_qa_aarch64.json

It can fect information about the last image built (nighlt) or an specific formal release
(like 'ER3' or similar).

By default, it'll return the compose for the QA image, but it can also show the compose for other
images like 'cki', 'ps' or 'developer'.

It also supports a board based images, that's it images to be flashed on boards like QDrive3 or
RideSX4 using the android boot system (aboot).

This script can be used standalone or its functions can be called from another script.
"""


import logging
import os
import sys
from http.client import HTTPConnection
from typing import Dict, Optional, Tuple

import requests
from requests.exceptions import RequestException

from .data_utils import generate_board_compose, populate_board_variables
from .request_utils import HEADER_NO_CACHE

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
if LOGLEVEL == "DEBUG":
    # Enable HTTP low level debug
    HTTPConnection.debuglevel = 1

VALID_IMAGES_FOR_TESTING = ["qa", "qm", "cki"]


class ImageInfoError(Exception):
    pass


def get_image_info(
    webserver_releases: str, release_name: str, image_name: str, arch: str, debug_kernel: bool
) -> Dict[str, str]:
    """
    Get the metadata for the image we want to test from a AMI_inof*.json file published
    at the webserver release alongside the published images.

    Args:
        webserver_releases (str): Base URL for the server where the file is being stored
            release_name (str): Name of the image's release. It could be either 'nightly' or
            a formal release like 'ER3'.
        image_name (str): Name of the image template used for building the images. It could be 'qa', 'cki',
            'developer' or 'minimal'.
        debug_kernel (srt): Does this image have the kernel-automotive-debug installed?

    Returns:
        Dict[str, str]: Dictionary with some metatada for the AMI published by the pipeline
    """
    if debug_kernel:
        ami_filename = f"AMI_info_{image_name}_debug_{arch}.json"
    else:
        ami_filename = f"AMI_info_{image_name}_{arch}.json"
    logging.debug(f"Using ami name: {ami_filename}")

    try:
        ami_info_url = f"{webserver_releases}/{release_name}/sample-images/{ami_filename}"
        response = requests.get(ami_info_url, headers=HEADER_NO_CACHE)
        response.raise_for_status()
    except RequestException as e:
        raise ImageInfoError(f"Error downloading the file from {ami_info_url}. Error: {e}")

    return response.json()


def board_compose(
    webserver_releases: str, release_name: str, image_key: str, arch: str, hw_target: str
) -> Tuple[str, str]:
    """
    Return a valid compose for board based images (images that boot on boards like QDrive3, RideSX4, Renesas, TI).
    The compose is a string but is formated as a JSON.

    Args:
        webserver_releases (str): Base URL for the server where the file is being stored
            release_name (str): Name of the image's release. It could be either 'nightly' or
            a formal release like 'ER3'.
        image_key (str): The AMI name taking from sample_images.
            For the board images, this name will be the directory where the images are located.
        arch (srt): The image's architecture. Right now 'aarch64' is the only one supported.
        hw_target (str): The code name for the board to be flashed. The valid boards and codes are:
            - QDrive3: 'qdrive3'
            - RideSX4: 'ridesx4'
            - Renesas: 'rcar_s4'
            - TI J7: 'ti-j784s4'
            - TI AM6: 'ti-am69sk'

    Returns:
        Tuple[str, str]: A tuple with two strings:
            - tf_pool: The Testing Farm pool for that type of boards
            - tf_compose: A escaped JSON-like string with the URLs for the necessary images
                to flash the OS to the board.
    """
    s3_upload_prefix, tf_pool = populate_board_variables("", "", arch, hw_target)
    base_url = f"{webserver_releases}/{release_name}/{s3_upload_prefix}/{image_key}"
    tf_compose = generate_board_compose(base_url=base_url, hw_target=hw_target)
    return tf_pool, tf_compose


def calculate_auto_compose(config: Optional[Dict[str, str]] = None) -> Optional[Tuple[str, str]]:
    """
    Calculate and return a string with a valid Testing Farm compose.

    It takes information from a 'config' dictionary passed as args or (if not provided), it takes
    the information from the environment.

    It'll update some items (IMAGE_NAME, IMAGE_TYPE, IMAGE_KEY and UUID) for the 'config' dictionary if
    it's passed as argument, but just if the HW_TARGET is not 'aws'.

    Args:
        config Optional[Dict[str, str]]: Dictionary with the program configuration. It should have
            some items (webserver_releases, RELEASE_NAME, DEBUG_KERNEL, IMAGE_NAME, ARCH, HW_TARGET).
            If not, it'll use the default values.

    Returns:
        Optional[Tuple[str, str]]: A tuple with two strings:
            - tf_pool: The Testing Farm pool for that type of boards
            - tf_compose: The Testing Farm compose for the requested image.
            It'll return None if there was a problem for getting the image information.
    """
    if not config:
        config = os.environ.copy()
    # Update these the config with these default values if they are not set
    release_name = config.setdefault("RELEASE_NAME", "nightly")
    image_name = config.setdefault("IMAGE_NAME", "qa")
    # Obtain some values to work with
    webserver_releases = config["webserver_releases"]
    debug_kernel = config.get("DEBUG_KERNEL", "false") == "true"
    arch = config.get("ARCH", "aarch64")
    hw_target = config.get("HW_TARGET", "aws")
    tf_pool = config.get("tf_pool", "")

    try:
        image_info = get_image_info(webserver_releases, release_name, image_name, arch, debug_kernel)
        config["IMAGE_KEY"] = image_info["ami_name"]
        config["UUID"] = image_info["UUID"]

        # Calculate and set values for board images
        if hw_target != "aws":
            if image_name not in VALID_IMAGES_FOR_TESTING:
                raise ImageInfoError(f"Error: the image {image_name} is not valid for testing packages.")
            # Save current values
            current_image_type = image_info["image_type"]
            # Change to the known defaults for aboot images
            default_build_target = "qemu"
            config.setdefault("IMAGE_TYPE", "regular")  # Set regular only if there is nor other value
            build_target = hw_target
            config["IMAGE_KEY"] = (
                config["IMAGE_KEY"]
                .replace(default_build_target, build_target)
                .replace(current_image_type, config["IMAGE_TYPE"])
            )
            if hw_target in ["qdrive3", "ridesx4"]:
                config["IMAGE_KEY"] += ".aboot"
            return board_compose(webserver_releases, release_name, config["IMAGE_KEY"], arch, hw_target)

        # Set or update the values at the config
        config["IMAGE_TYPE"] = image_info["image_type"]

        return tf_pool, config["IMAGE_KEY"]
    except ImageInfoError as e:
        logging.error(e)
        return None


def main():
    _, compose = calculate_auto_compose()
    if not compose:
        # Exit with error, but different from 1, in case the job allow failure with 1
        sys.exit(2)
    print(compose)


if __name__ == "__main__":
    main()
