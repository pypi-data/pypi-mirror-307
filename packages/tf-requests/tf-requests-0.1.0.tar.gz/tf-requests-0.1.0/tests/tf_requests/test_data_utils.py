import json
from unittest.mock import patch

import pytest
import requests_mock

from tf_requests.data_utils import (
    determine_board_base_url,
    determine_tf_compose,
    generate_board_compose,
    get_package_nvr,
    populate_board_variables,
)

# Test determine_board_base_url()


@pytest.mark.parametrize(
    "release_name, webserver_workspaces, workspace_id, s3_upload_prefix, image_key, webserver_releases, expected",
    [
        # Test scenario for pipelines-as-code pipeline (release_name is None)
        (
            None,
            "https://workspaces.com",
            "123",
            "prefix",
            "key",
            "https://releases.com",
            "https://workspaces.com/123/prefix/key",
        ),
        # Test scenario for package-level-pipeline (release_name is provided)
        (
            "release1",
            "https://workspaces.com",
            "123",
            "prefix",
            "key",
            "https://releases.com",
            "https://releases.com/release1/prefix/key",
        ),
    ],
)
def test_get_board_base_url(
    release_name,
    webserver_workspaces,
    workspace_id,
    s3_upload_prefix,
    image_key,
    webserver_releases,
    expected,
):
    result = determine_board_base_url(
        release_name,
        webserver_workspaces,
        workspace_id,
        s3_upload_prefix,
        image_key,
        webserver_releases,
    )
    assert result == expected


# Test generate_board_compose()


@pytest.fixture
def aboot_compose():
    base_url = "https://example.com"
    data_structure = generate_board_compose(base_url, "ridesx4")
    return data_structure


@pytest.fixture
def renesas_compose():
    base_url = "https://example.com"
    data_structure = generate_board_compose(base_url, "rcar_s4")
    return data_structure


def test_valid_json_string(aboot_compose):
    try:
        json.loads(aboot_compose)
    except json.JSONDecodeError as e:
        pytest.fail(f"Output is not a valid JSON. Error: {e}")


def test_valid_aboot_json_keys(aboot_compose):
    data = json.loads(aboot_compose)

    assert data["boot_image"] == "https://example.com.aboot/aboot.img.xz"
    assert data["boot_checksum"] == "https://example.com.aboot/aboot.img.xz.sha256"
    assert data["root_image"] == "https://example.com.aboot/rootfs.simg.xz"
    assert data["root_checksum"] == "https://example.com.aboot/rootfs.simg.xz.sha256"


def test_valid_renesas_json_keys(renesas_compose):
    data = json.loads(renesas_compose)

    assert data["disk_image"] == "https://example.com.raw.xz"
    assert data["disk_checksum"] == "https://example.com.raw.xz.sha256"


# Test determine_tf_compose()

# FIXME: Fix the composes for aboot
# Also check that  actualy looks like this:
# "{\"boot_image\":\"[MASKED]/5327074.fe8f00c5/QDrive3/auto-osbuild-qdrive3-rhel9-qa-regular-aarch64-5327074.fe8f00c5.aboot/aboot.img.xz\",\"boot_checksum\":\"[MASKED]/5327074.fe8f00c5/QDrive3/auto-osbuild-qdrive3-rhel9-qa-regular-aarch64-5327074.fe8f00c5.aboot/aboot.img.xz.sha256\",\"root_image\":\"[MASKED]/5327074.fe8f00c5/QDrive3/auto-osbuild-qdrive3-rhel9-qa-regular-aarch64-5327074.fe8f00c5.aboot/rootfs.simg.xz\",\"root_checksum\":\"[MASKED]/5327074.fe8f00c5/QDrive3/auto-osbuild-qdrive3-rhel9-qa-regular-aarch64-5327074.fe8f00c5.aboot/rootfs.simg.xz.sha256\"}"


@pytest.mark.parametrize(
    "tf_compose, action, image_key, arch, stream, build_format, expected",
    [
        ("build_compose", "BUILD", "image_key", "x86_64", "UPSTREAM", "", "build_compose"),
        ("build_compose", "BUILD", "image_key", "aarch64", "UPSTREAM", "", "build_compose-aarch64"),
        ("build_compose", "TEST", "image_key", "x86_64", "UPSTREAM", "", "image_key"),
        ("build_compose", "TEST", "image_key", "aarch64", "UPSTREAM", "", "image_key"),
        ("build_compose", "BUILD", "image_key", "x86_64", "DOWNSTREAM", "", "build_compose"),
        ("build_compose", "BUILD", "image_key", "aarch64", "DOWNSTREAM", "", "build_compose"),
        ("build_compose", "TEST", "image_key", "x86_64", "DOWNSTREAM", "", "image_key"),
        ("build_compose", "TEST", "image_key", "aarch64", "DOWNSTREAM", "", "image_key"),
        ("aboot_compose", "TEST", "image_key", "x86_64", "UPSTREAM", "aboot", "aboot_compose"),
        ("aboot_compose", "TEST", "image_key", "aarch64", "DOWNSTREAM", "aboot", "aboot_compose"),
        ("aboot_compose", "TEST", "image_key", "x86_64", "UPSTREAM", "aboot.simg", "aboot_compose"),
        (
            "aboot_compose",
            "TEST",
            "image_key",
            "aarch64",
            "DOWNSTREAM",
            "aboot.simg",
            "aboot_compose",
        ),
    ],
)
def test_determine_tf_compose_case(tf_compose, action, image_key, arch, stream, build_format, expected):
    result = determine_tf_compose(tf_compose, action, image_key, arch, stream, build_format)

    assert result == expected


# Test populate_board_variables


@pytest.mark.parametrize(
    "s3_upload_prefix, tf_pool, arch, hw_target, expected_s3_upload_prefix, expected_tf_pool",
    [
        ("default_prefix", "", "aarch64", "qdrive3", "QDrive3", "qdrive3-atc"),
        ("default_prefix", "", "other_arch", "qdrive3", "QDrive3", ""),
        ("default_prefix", "", "aarch64", "ridesx4", "RideSX4", "ride4-atc"),
        ("default_prefix", "", "other_arch", "ridesx4", "RideSX4", ""),
        ("default_prefix", "", "aarch64", "ti-j784s4", "TI", "ti-j784s4-atc"),
        ("default_prefix", "", "other_arch", "ti-j784s4", "TI", ""),
        ("default_prefix", "", "aarch64", "ti-am69sk", "TI", "ti-am69sk-atc"),
        ("default_prefix", "", "other_arch", "ti-am69sk", "TI", ""),
    ],
)
def test_populate_board_variables(
    s3_upload_prefix, tf_pool, arch, hw_target, expected_s3_upload_prefix, expected_tf_pool
):
    s3_upload_prefix, tf_pool = populate_board_variables(s3_upload_prefix, tf_pool, arch, hw_target)
    assert s3_upload_prefix == expected_s3_upload_prefix
    assert tf_pool == expected_tf_pool


def test_populate_unknown_board_variables():
    s3_upload_prefix = "default_prefix"
    tf_pool = ""
    arch = "aarch64"
    hw_target = "unknown_board"
    expected_exit_code = 2

    class ExitException(Exception):
        pass

    with patch("sys.exit", side_effect=ExitException) as mock_exit:
        try:
            s3_upload_prefix, tf_pool = populate_board_variables(s3_upload_prefix, tf_pool, arch, hw_target)
        except ExitException:
            pass

        mock_exit.assert_called_with(expected_exit_code)


# Test get_package_nvr


mock_config = {"webserver_releases": "http://example.com/releases", "release_name": "sample_release", "arch": "aarch64"}


def generate_mock_manifest(release_name, package_nvr):
    """Generate a mock manifest based on the provided release name and NVR."""
    return {
        "cdn": {
            "products": {
                "9999": {
                    "Repo Paths": {
                        f"/in-vehicle-os-9/{release_name}/repos/RHIVOS/compose/RHIVOS/source/tree": {
                            "RPMs": [
                                "glibc-langpack-gu-2.34-83.el9_3.5.src.rpm",
                                f"{package_nvr}.src.rpm",
                            ]
                        }
                    }
                }
            }
        }
    }


@pytest.mark.parametrize(
    "release_name, mock_response, package_name, expected_result, expected_exception",
    [
        # Successful extractions
        (
            "ER3.1",
            {"json": generate_mock_manifest("ER3.1", "glibc-2.34-83.el9_3.5")},
            "glibc",
            "glibc-2.34-83.el9_3.5",
            None,
        ),
        (
            "ER4",
            {"json": generate_mock_manifest("ER4", "glibc-2.34-83.el9_3.5")},
            "glibc",
            "glibc-2.34-83.el9_3.5",
            None,
        ),
        (
            "ER5",
            {"json": generate_mock_manifest("ER5", "glibc-2.34-83.el9_3.5")},
            "glibc",
            "glibc-2.34-83.el9_3.5",
            None,
        ),
        (
            "RHIVOS0.17",
            {"json": generate_mock_manifest("RHIVOS0.17", "glibc-2.34-83.el9_3.5")},
            "glibc",
            "glibc-2.34-83.el9_3.5",
            None,
        ),
        (
            "RHIVOS0.20",
            {"json": generate_mock_manifest("RHIVOS0.20", "glibc-2.34-83.el9_3.5")},
            "glibc",
            "glibc-2.34-83.el9_3.5",
            None,
        ),
        (
            "nightly",
            {"json": generate_mock_manifest("nightly", "glibc-2.34-83.el9_3.5")},
            "glibc",
            "glibc-2.34-83.el9_3.5",
            None,
        ),
        # Successul extration with package that need escape (with + character)
        (
            "nightly",
            {"json": generate_mock_manifest("nightly", "memtest86+-5.31-0.4.beta.el9")},
            "memtest86+",
            "memtest86+-5.31-0.4.beta.el9",
            None,
        ),
        # Failures
        (
            "sample_release",
            {"json": generate_mock_manifest("sample_release", "glibc-2.34-83.el9_3.5")},
            "nonexistent_package",
            None,
            ValueError,
        ),
        ("sample_release", {"status_code": 404}, "glibc", None, Exception),
        ("sample_release", {"text": "not a json"}, "glibc", None, ValueError),
        ("sample_release", {"json": {"unexpected": "structure"}}, "glibc", None, ValueError),
    ],
)
def test_get_package_nvr(release_name, mock_response, package_name, expected_result, expected_exception):
    mock_config["release_name"] = release_name
    base_url = f"{mock_config['webserver_releases']}/{release_name}"
    # It should try the new URL and if it fails, then try the old one
    if release_name in ["ER4", "ER5", "RHIVOS0.19", "RHIVOS0.20", "nightly"]:
        # Use the new path for some new releases
        url = f"{base_url}/cat-manifests/manifest-source.json"
    else:
        # Use the old path for the rest of releases
        url = f"{base_url}/cat-manifest/manifest.json"
    with requests_mock.Mocker() as m:
        # Mock all URl by default to error (404)
        # This allow to use a bad URL first, to fail and try the second one
        m.register_uri("GET", requests_mock.ANY, status_code=404)
        # Mock with the mock response only the one we want to test
        m.get(url, **mock_response)
        if expected_exception:
            with pytest.raises(expected_exception):
                get_package_nvr(mock_config, package_name)
        else:
            result = get_package_nvr(mock_config, package_name)
            assert result == expected_result
