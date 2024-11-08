import json
from unittest.mock import patch

import pytest
import requests_mock

from tf_requests.get_auto_compose import (
    ImageInfoError,
    board_compose,
    calculate_auto_compose,
    get_image_info,
)

# Sample URLs and data
WEBSERVER_RELEASES = "http://example.com/releases"
RELEASE_NAME = "ER0"
IMAGE_NAME = "minimal"
UUID = "00000000-abcabcab"
ARCH = "aarch64"
IMAGE_TYPE = "ostree"
BUILD_TARGET = "qemu"
BUILD_FORMAT = "img"
IMAGE_KEY = f"auto-osbuild-{BUILD_TARGET}-autosd9-{IMAGE_NAME}-{IMAGE_TYPE}-{ARCH}-{UUID}"
AMI_NAME = IMAGE_KEY

# Mocked response data
MOCK_RESPONSE = {"ami_id": "ami-12345678", "region": "us-east-1"}

# Test get_image_info


@pytest.mark.parametrize(
    "debug_kernel, expected_filename",
    [
        (True, "AMI_info_minimal_debug_aarch64.json"),
        (False, "AMI_info_minimal_aarch64.json"),
    ],
)
def test_get_image_info(debug_kernel, expected_filename):
    expected_url = f"{WEBSERVER_RELEASES}/{RELEASE_NAME}/sample-images/{expected_filename}"

    with requests_mock.Mocker() as mocker:
        mocker.get(expected_url, json=MOCK_RESPONSE)

        result = get_image_info(WEBSERVER_RELEASES, RELEASE_NAME, IMAGE_NAME, ARCH, debug_kernel)
        assert result == MOCK_RESPONSE


def test_get_image_info_failure():
    failing_url = f"{WEBSERVER_RELEASES}/{RELEASE_NAME}/sample-images/AMI_info_minimal_aarch64.json"

    with requests_mock.Mocker() as mocker:
        mocker.get(failing_url, status_code=404)

    with pytest.raises(ImageInfoError):
        get_image_info(WEBSERVER_RELEASES, RELEASE_NAME, IMAGE_NAME, ARCH, False)


# Test board_compose


@pytest.mark.parametrize(
    "hw_target, expected_prefix",
    [
        ("qdrive3", "QDrive3"),
        ("ridesx4", "RideSX4"),
    ],
)
def test_aboot_compose(hw_target, expected_prefix):
    _, compose = board_compose(WEBSERVER_RELEASES, RELEASE_NAME, IMAGE_KEY, ARCH, hw_target)
    assert json.loads(compose)  # Check it's a valid json
    data = json.loads(compose)

    base_url = "http://example.com/releases/ER0"
    assert data["boot_image"] == f"{base_url}/{expected_prefix}/{IMAGE_KEY}.aboot/aboot.img.xz"
    assert data["boot_checksum"] == f"{base_url}/{expected_prefix}/{IMAGE_KEY}.aboot/aboot.img.xz.sha256"
    assert data["root_image"] == f"{base_url}/{expected_prefix}/{IMAGE_KEY}.aboot/rootfs.simg.xz"
    assert data["root_checksum"] == f"{base_url}/{expected_prefix}/{IMAGE_KEY}.aboot/rootfs.simg.xz.sha256"


@pytest.mark.parametrize(
    "hw_target, expected_prefix",
    [
        ("rcar_s4", "Renesas"),
    ],
)
def test_renesas_compose(hw_target, expected_prefix):
    _, compose = board_compose(WEBSERVER_RELEASES, RELEASE_NAME, IMAGE_KEY, ARCH, hw_target)
    assert json.loads(compose)  # Check it's a valid json
    data = json.loads(compose)

    base_url = "http://example.com/releases/ER0"
    assert data["disk_image"] == f"{base_url}/{expected_prefix}/{IMAGE_KEY}.raw.xz"
    assert data["disk_checksum"] == f"{base_url}/{expected_prefix}/{IMAGE_KEY}.raw.xz.sha256"


# Test calculate_auto_compose

# Mocking the get_image_info function to return a controlled response
mock_image_info = {"ami_name": AMI_NAME, "image_type": IMAGE_TYPE, "UUID": UUID}


@pytest.mark.parametrize(
    "config, expected",
    [
        # config passed and has all the required items
        (
            {
                "webserver_releases": "http://example.com/releases",
                "RELEASE_NAME": RELEASE_NAME,
                "DEBUG_KERNEL": "false",
                "IMAGE_NAME": IMAGE_NAME,
                "ARCH": ARCH,
                "HW_TARGET": "aws",
                "x_stream": None,
            },
            AMI_NAME,
        ),
        # config passed but is missing some items
        (
            {
                "webserver_releases": "http://example.com/releases",
                "x_stream": None,
            },
            AMI_NAME,
        ),
    ],
)
def test_calculate_auto_compose_config(config, expected):
    with patch("tf_requests.get_auto_compose.get_image_info", return_value=mock_image_info):
        _, compose = calculate_auto_compose(config)
        assert compose == expected


@pytest.mark.parametrize(
    "env_vars, config, expected",
    [
        # config not passed but all required items are in os.environ
        (
            {
                "webserver_releases": "http://example.com/releases",
                "RELEASE_NAME": RELEASE_NAME,
                "DEBUG_KERNEL": "false",
                "IMAGE_NAME": IMAGE_NAME,
                "ARCH": ARCH,
                "HW_TARGET": "aws",
                "x_stream": None,
            },
            None,
            AMI_NAME,
        ),
        # config not passed but some required items are missing in os.environ
        (
            {
                "webserver_releases": "http://example.com/releases",
                "x_stream": None,
            },
            None,
            AMI_NAME,
        ),
    ],
)
def test_calculate_auto_compose_env_vars(env_vars, config, expected):
    with (
        patch("os.environ", new=env_vars),
        patch("tf_requests.get_auto_compose.get_image_info", return_value=mock_image_info),
    ):
        _, compose = calculate_auto_compose(config)
        assert compose == expected


# Prepare mocks for the calculate_auto_compose function
# That function converts the IMAGE_NAME to 'qa' unless it's explicitly set to other
AMI_NAME_QA = f"auto-osbuild-qemu-autosd9-qa-ostree-{ARCH}-{UUID}"
mock_image_info_qa = {"ami_name": AMI_NAME_QA, "image_type": "ostree", "UUID": UUID}

IMAGE_KEY_QDRIVE3_QA = f"auto-osbuild-qdrive3-autosd9-qa-regular-{ARCH}-{UUID}"
mock_qdrive3_compose = {
    "boot_image": f"http://example.com/releases/ER0/QDrive3/{IMAGE_KEY_QDRIVE3_QA}.aboot/aboot.img.xz",
    "boot_checksum": f"http://example.com/releases/ER0/QDrive3/{IMAGE_KEY_QDRIVE3_QA}.aboot/aboot.img.xz.sha256",
    "root_image": f"http://example.com/releases/ER0/QDrive3/{IMAGE_KEY_QDRIVE3_QA}.aboot/rootfs.simg.xz",
    "root_checksum": f"http://example.com/releases/ER0/QDrive3/{IMAGE_KEY_QDRIVE3_QA}.aboot/rootfs.simg.xz.sha256",
}
IMAGE_KEY_RIDE4_QA = f"auto-osbuild-ridesx4-autosd9-qa-regular-{ARCH}-{UUID}"
mock_ridesx4_compose = {
    "boot_image": f"http://example.com/releases/ER0/RideSX4/{IMAGE_KEY_RIDE4_QA}.aboot/aboot.img.xz",
    "boot_checksum": f"http://example.com/releases/ER0/RideSX4/{IMAGE_KEY_RIDE4_QA}.aboot/aboot.img.xz.sha256",
    "root_image": f"http://example.com/releases/ER0/RideSX4/{IMAGE_KEY_RIDE4_QA}.aboot/rootfs.simg.xz",
    "root_checksum": f"http://example.com/releases/ER0/RideSX4/{IMAGE_KEY_RIDE4_QA}.aboot/rootfs.simg.xz.sha256",
}


@pytest.mark.parametrize(
    "hw_target, expected",
    [
        # hw_target == aws
        ("aws", AMI_NAME_QA),
        # hw_target != aws AND in ['qdrive3, 'ridesx4']
        ("qdrive3", json.dumps(mock_qdrive3_compose)),
        ("ridesx4", json.dumps(mock_ridesx4_compose)),
    ],
)
def test_calculate_auto_compose_hw_target(hw_target, expected):
    config = {
        "webserver_releases": "http://example.com/releases",
        "RELEASE_NAME": RELEASE_NAME,
        "DEBUG_KERNEL": "false",
        "ARCH": ARCH,
        "HW_TARGET": hw_target,
        "x_stream": None,
    }
    with patch("tf_requests.get_auto_compose.get_image_info", return_value=mock_image_info_qa):
        _, compose = calculate_auto_compose(config)
        assert compose == expected


def test_calculate_auto_compose_hw_target_not_supported():
    config = {
        "webserver_releases": "http://example.com/releases",
        "RELEASE_NAME": RELEASE_NAME,
        "DEBUG_KERNEL": "false",
        "ARCH": ARCH,
        "HW_TARGET": "not_supported",
        "x_stream": None,
    }
    with patch(
        "tf_requests.get_auto_compose.get_image_info",
        side_effect=ImageInfoError(),
    ):
        result = calculate_auto_compose(config)
        assert result is None
