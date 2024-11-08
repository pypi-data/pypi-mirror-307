import argparse
from unittest.mock import MagicMock, Mock, call, mock_open, patch

import pytest
import requests_mock

from tf_requests.tf_requests import (
    ENV_VARS_FILE,
    TEST_VALID_CODES,
    TESTS_RESULTS_DIR,
    adjust_for_package_testing,
    cli,
    fail_on_error,
    generate_payload,
    get_board_data,
    load_configuration,
    main,
    make_request_and_wait,
    post_process_results,
    save_env_vars,
    store_results,
)


def test_cli():
    # Mock command line arguments
    test_args = ["tf_requests.py", "--variables", "VAR1,VAR2", "--secrets", "SECRET1,SECRET2"]

    with patch("sys.argv", test_args):
        args = cli()
        assert isinstance(args.variables, str)
        assert isinstance(args.secrets, str)
        assert isinstance(args.show_payload, bool)
        assert args.variables == "VAR1,VAR2"
        assert args.secrets == "SECRET1,SECRET2"
        assert args.show_payload is False


def test_cli_show_payload():
    # Mock command line arguments
    test_args = ["tf_requests.py", "--variables", "VAR1,VAR2", "--show-payload"]

    with patch("sys.argv", test_args):
        args = cli()
        assert isinstance(args.variables, str)
        assert isinstance(args.show_payload, bool)
        assert args.variables == "VAR1,VAR2"
        assert args.secrets is None
        assert args.show_payload is True


# Mock argparse.Namespace data
mock_arg_data = {
    "secrets": "SECRET_1,SECRET_2",
    "variables": "VARIABLE_1,VARIABLE_2,OS_OPTIONS",
    "show_payload": True,
}

# Mock environment variables
mock_os_environ = {
    "TF_API_KEY": "test_api_key",
    "TF_ENDPOINT": "http://api.testing-farmc.com/",
    "CI_REPO_URL": "http://example.com/repo.git",
    "CI_REF": "main",
    "TMT_PLAN": "/plans/tests",
    "ARCH": "aarch64",
    "IMAGE_KEY": "minimal",
    "TF_COMPOSE": "RHEL-9",
    "WEBSERVER_RELEASES": "http://rebserve-releases.com",
    "SECRET_1": "value_1",
    "SECRET_2": "value_2",
    "VARIABLE_1": "var_1",
    "VARIABLE_2": "var_2",
    "OS_OPTIONS": 'osname="centos" uefi_vendor="centos"',
}


# Test the load_configuration function
def test_load_configuration():
    args = argparse.Namespace(**mock_arg_data)
    with patch.dict("os.environ", mock_os_environ):
        secrets, variables, config = load_configuration(args)
        assert config["api_key"] == "test_api_key"
        assert config["test__fmf__url"] == "http://example.com/repo.git"
        assert secrets["SECRET_1"] == "value_1"
        assert variables["VARIABLE_1"] == "var_1"
        assert variables["OS_OPTIONS"] == 'osname="centos" uefi_vendor="centos"'


# Test the load_configuration function with X_STREAM
@pytest.mark.parametrize(
    "webserver_releases, x_stream, expected_webserver_releases",
    [
        ("http://webserver-releases.com", None, "http://webserver-releases.com"),
        ("http://webserver-releases.com", "PRODUCT-1", "http://webserver-releases.com/PRODUCT-1"),
    ],
)
def test_load_configuration_x_stream(webserver_releases, x_stream, expected_webserver_releases):
    mock_os_environ["WEBSERVER_RELEASES"] = webserver_releases
    mock_arg_data["variables"] += ",WEBSERVER_RELEASES"  # Add to the list of variables
    if x_stream:
        mock_os_environ["X_STREAM"] = x_stream
        mock_arg_data["variables"] += ",X_STREAM"  # Add to the list of variables
    args = argparse.Namespace(**mock_arg_data)
    with patch.dict("os.environ", mock_os_environ):
        _, _, config = load_configuration(args)
        assert config["webserver_releases"] == expected_webserver_releases


# Test the adjust_for_package_testing function
@pytest.mark.parametrize(
    "config, obtain_pkg_nvr, expected_pkg_nvr",
    [
        ({"PACKAGE_NAME": "glibc", "IMAGE_KEY": "12345"}, "glibc-2.34-83.el9_3.5", "glibc-2.34-83.el9_3.5"),
        (
            {"PACKAGE_NAME": "glibc", "PACKAGE_NVR": "glibc-2.35.el9", "IMAGE_KEY": "12345"},
            "glibc-2.34-83.el9_3.5",
            "glibc-2.35.el9",
        ),
        ({"PACKAGE_NAME": "unsupported", "IMAGE_KEY": "12345"}, "", ""),
    ],
)
def test_adjust_for_package_testing(config, obtain_pkg_nvr, expected_pkg_nvr):
    variables = {}
    with (
        patch("tf_requests.tf_requests.get_package_nvr") as mock_get_nvr,
        patch("tf_requests.tf_requests.calculate_auto_compose") as mock_calculate,
    ):
        mock_get_nvr.return_value = obtain_pkg_nvr
        mock_calculate.return_value = "tf_pool", "tf_compose"
        adjust_for_package_testing(config, variables)
        assert "PACKAGE_NVR" in config
        assert "PACKAGE_NVR" in variables
        assert "IMAGE_KEY" in config
        assert "IMAGE_KEY" in variables
        assert config["PACKAGE_NVR"] == expected_pkg_nvr
        assert variables["PACKAGE_NVR"] == expected_pkg_nvr
        assert config["IMAGE_KEY"] != ""
        assert variables["IMAGE_KEY"] != ""


# Test the generate_payload function
mock_variables = {"VAR_1": "value 1"}

mock_secrets = {"secret": "password"}

mock_config = {
    "api_key": "test_api_key",
    "test__fmf__url": "http://example.com/repo.git",
    "arch": "aarch64",
    "hw_target": "aws",
    "IMAGE_TYPE": "ostree",
    "IMAGE_NAME": "minimal",
    "tf_pool": "",
    "tf_compose": "CentosStream9",
    "environments__tmt__context__distro": "centos",
    "environments__hardware__hostname": "beaker-vm1",
    "settings__pipeline__timeout": 120,
    "environments__settings__provisioning__tags__ArtemisOneShotOnly": True,
    "settings__pipeline__provision-error-failed-result": False,
}


def test_generate_payload():
    payload = generate_payload(mock_config, mock_variables, mock_secrets)
    assert payload["api_key"] == "test_api_key"
    assert payload["test"]["fmf"]["url"] == "http://example.com/repo.git"
    assert payload["environments"][0]["variables"]["VAR_1"] == "value 1"
    assert payload["environments"][0]["secrets"]["secret"] == "password"
    assert payload["environments"][0]["tmt"]["context"]["distro"] == "centos"
    assert payload["environments"][0]["tmt"]["context"]["arch"] == "aarch64"
    assert payload["environments"][0]["tmt"]["context"]["hw_target"] == "aws"
    assert payload["environments"][0]["tmt"]["context"]["image_type"] == "ostree"
    assert payload["environments"][0]["tmt"]["context"]["image_name"] == "minimal"
    assert payload["environments"][0]["hardware"]["hostname"] == "beaker-vm1"
    assert payload["settings"]["pipeline"]["timeout"] == 120
    assert payload["environments"][0]["settings"]["provisioning"]["tags"]["ArtemisOneShotOnly"]
    assert not payload["settings"]["pipeline"]["provision-error-failed-result"]


# Test the make_request_and_wait function
mock_response_success = {
    "id": "1234-abcd",
    "created": "2020-12-18T20:46:00.392227",
    "state": "complete",
}

mock_response_error = {"detail": [{"loc": ["0"], "msg": "Invalid request", "type": "error"}]}

mock_payload = {"value": "key"}


def test_make_request_and_wait():
    with requests_mock.Mocker() as m:
        m.post("http://tf_endpoint.com/", json=mock_response_success, status_code=201)
        m.get("http://tf_endpoint.com/1234-abcd", json=mock_response_success, status_code=200)
        result = make_request_and_wait("http://tf_endpoint.com", mock_payload)
        assert result["id"] == "1234-abcd"


# Test the make_request_and_wait function for an error
def test_make_request_and_wait_error():
    with requests_mock.Mocker() as m:
        m.post("http://tf_endpoint.com/", json=mock_response_success, status_code=201)
        m.get("http://tf_endpoint.com/1234-abcd", json=mock_response_error, status_code=422)
        with pytest.raises(ValueError, match="Invalid request"):
            make_request_and_wait("http://tf_endpoint.com", "1234-abcd")


# Test the get aboot data function
mock_config_aboot = {
    "api_key": "test_api_key",
    "upload_prefix": "images",
    "tf_pool": "",
    "arch": "aarch64",
    "hw_target": "qdrive3",
    "WEBSERVER_WORKSPACES": "http://workspaces.com",
    "WORKSPACE_ID": "12345",
    "IMAGE_KEY": "image-key-12345",
    "webserver_releases": "http://releases.com",
    "release_name": None,
}

expected_aboot_tf_compose = (
    '{"boot_image": "http://workspaces.com/12345/QDrive3/image-key-12345.aboot/aboot.img.xz", '
    '"boot_checksum": "http://workspaces.com/12345/QDrive3/image-key-12345.aboot/aboot.img.xz.sha256", '
    '"root_image": "http://workspaces.com/12345/QDrive3/image-key-12345.aboot/rootfs.simg.xz", '
    '"root_checksum": "http://workspaces.com/12345/QDrive3/image-key-12345.aboot/rootfs.simg.xz.sha256"}'
)


def test_aboot_data_with_valid_input():
    tf_pool, tf_compose = get_board_data(mock_config_aboot)
    assert tf_pool == "qdrive3-atc"
    assert tf_compose == expected_aboot_tf_compose


def test_aboot_data_missing_webserver_releases_raises_error():
    # Remove the webserver_releases key
    mock_config = mock_config_aboot.copy()
    del mock_config["webserver_releases"]

    with pytest.raises(ValueError, match="'WEBSERVER_RELEASES' can't be empty for a board tests"):
        get_board_data(mock_config)


def mock_response(*args, **kwargs):
    mock = Mock()
    mock.iter_content.return_value = iter([b"chunk1", b"chunk2"])
    mock.raise_for_status.return_value = None  # Ensure that raise_for_status does not raise an exception
    return mock


@pytest.mark.parametrize(
    "download_return_value, expected_log_method, expected_log_message",
    [
        (True, "info", f"The JUnit xml file was successfully stored at '{TESTS_RESULTS_DIR}/test-results-junit.xml'"),
        (False, "error", "There was an error and the report file wasn't stored locally"),
    ],
)
def test_store_results_download(download_return_value, expected_log_method, expected_log_message):
    results = {
        "result": {"overall": "passed"},
        "run": {"artifacts": "https://example.com/artifacts"},
    }

    with (
        patch("logging.info") as mock_info,
        patch("logging.error") as mock_error,
        patch("tf_requests.tf_requests.download_file", return_value=download_return_value),
    ):
        store_results(results)

        log_method_mapping = {
            "info": mock_info,
            "error": mock_error,
        }

        # Check if the expected log message is among the calls
        assert call(expected_log_message) in log_method_mapping[expected_log_method].call_args_list


def test_store_results_early_return():
    # Example data that should trigger the early return
    results = {
        "result": {"overall": "INVALID_CODE"},  # Assuming this is not in TEST_VALID_CODES
        "run": {"artifacts": "https://example.com/artifacts"},
    }

    with patch("logging.error") as mock_error, patch("logging.info") as mock_info:
        store_results(results)

        # Assert that logging.error was called with the expected message
        mock_error.assert_called_once_with("As the job failed, there is no test report to download")

        # Assert that logging.info was not called, indicating that the function returned early
        mock_info.assert_not_called()


# Test save_env_vars


sample_results = {
    "run": {"artifacts": "https://example.com/artifacts"},
    "result": {"overall": "passed"},
    "test": {"fmf": {"name": "sample_name", "url": "https://example.com/fmf_path"}},
}

sample_config = {
    "artifacts_workdir_urls": '[{"name":"/package/plans/test"}, {"workdir":"http://web.com/path/to/workdir"}]',
    "release_name": "ER4",
    "IMAGE_NAME": "sample_image",
    "IMAGE_KEY": "sample_key",
    "IMAGE_TYPE": "sample_type",
    "arch": "x86_64",
    "UUID": "1234-5678",
    "OS_PREFIX": "RHEL",
    "OS_VERSION": "9",
    "stream": "stream_value",
    "build_format": "qcow2",
    "hw_target": "generic",
    "PACKAGE_NAME": "sample_package",
    "PACKAGE_NVR": "sample_package-1.0.0",
}

# Expected output for the file based on the sample input
expected_output = """\
ARTIFACTS_URL=https://example.com/artifacts
ARTIFACTS_WORKDIR_URLS='[{"name":"/package/plans/test"}, {"workdir":"http://web.com/path/to/workdir"}]'
RESULT=passed
RELEASE_NAME=ER4
IMAGE_NAME=sample_image
IMAGE_KEY=sample_key
IMAGE_TYPE=sample_type
IMAGE_ARCH=x86_64
IMAGE_UUID=1234-5678
OS_PREFIX=RHEL
OS_VERSION=9
STREAM=stream_value
BUILD_FORMAT=qcow2
HW_TARGET=generic
TESTS_RESULTS_DIR=tests_results
TMT_PLAN_NAME=sample_name
TMT_PLAN_PATH=https://example.com/fmf_path
PACKAGE_NAME=sample_package
PACKAGE_NVR=sample_package-1.0.0
"""


def test_save_env_vars_success():
    m = mock_open()
    with patch("builtins.open", m), patch("logging.info") as mock_info:
        save_env_vars(sample_results, sample_config)

        # Extract the written lines
        written_lines = [call_args[0][0].strip() for call_args in m().write.call_args_list]

        # Check if all expected lines are present in the written lines
        for expected_line in expected_output.strip().split("\n"):
            assert expected_line in written_lines
        mock_info.assert_called_once_with(f"ENV variables stored at '{ENV_VARS_FILE}' for future use")


def test_save_env_vars_file_error():
    m = mock_open()
    m.side_effect = IOError("Permission denied")
    with patch("builtins.open", m), patch("logging.error") as mock_error:
        save_env_vars(sample_results, sample_config)

        mock_error.assert_called_once_with("File operation error: Permission denied")


# Test fail_on_error


mock_results = {
    "id": "12345",
    "result": {"overall": "passed", "summary": "Some message"},
    "run": {"artifacts": "http://example.com/report"},
}


@pytest.mark.parametrize(
    "result, debug_msg, error_msg, exit_code",
    [
        ("passed", "Test result: passed", "", 0),
        ("failed", "Test result: failed", "", 0),
        (
            "error",
            "Test result: error",
            "There has been an error in Testing Farm with code 'error'",
            10,
        ),
        ("foo", "Test result: foo", "There has been an uknown error with code 'foo'", 15),
    ],
)
def test_fail_on_error(result, debug_msg, error_msg, exit_code):
    mock_results["result"]["overall"] = result

    class ExitException(Exception):
        pass

    with (
        patch("logging.debug") as mock_log_debug,
        patch("logging.error") as mock_log_error,
        patch("sys.exit", side_effect=ExitException) as mock_exit,
    ):
        try:
            fail_on_error(mock_results)
        except ExitException:
            pass

        mock_log_debug.assert_any_call(debug_msg)
        mock_exit.assert_called_with(exit_code)

        # Only for non valid result codes
        if mock_results["result"]["overall"] not in TEST_VALID_CODES:
            mock_log_error.assert_any_call(error_msg)


# Test post_process_results


@pytest.mark.parametrize(
    "action, expected_calls",
    [
        (
            "TEST",
            {
                "display_results": 1,
                "get_artifacts_workdir_urls": 1,
                "store_results": 1,
                "save_env_vars": 1,
                "fail_on_error": 1,
            },
        ),
        (
            "BUILD",
            {
                "display_results": 1,
                "get_artifacts_workdir_urls": 1,
                "store_results": 0,
                "save_env_vars": 1,
                "fail_on_error": 1,
            },
        ),
    ],
)
# Mocking the used functions to test the main flow
@patch("tf_requests.tf_requests.fail_on_error")
@patch("tf_requests.tf_requests.save_env_vars")
@patch("tf_requests.tf_requests.store_results")
@patch("tf_requests.tf_requests.get_artifacts_workdir_urls")
@patch("tf_requests.tf_requests.display_results")
def test_post_process_results(
    mock_display_results,
    mock_get_artifacts_workdir_urls,
    mock_store_results,
    mock_save_env_vars,
    mock_fail_on_error,
    action,
    expected_calls,
):
    mock_results = {"id": "12345", "result": {"overall": "passed"}}
    mock_get_artifacts_workdir_urls.return_value = [{"name": "name", "workdir": "workdir"}]
    post_process_results(mock_results, {"action": action})

    assert mock_display_results.call_count == expected_calls["display_results"]
    assert mock_get_artifacts_workdir_urls.call_count == expected_calls["get_artifacts_workdir_urls"]
    assert mock_store_results.call_count == expected_calls["store_results"]
    assert mock_save_env_vars.call_count == expected_calls["save_env_vars"]
    assert mock_fail_on_error.call_count == expected_calls["fail_on_error"]


# Test main()


@pytest.mark.parametrize(
    "config, mock_args, test_result, expected_calls",
    [
        (
            {
                "action": "TEST",
                "hw_target": "qdrive3",
                "PACKAGE_NAME": "glibc",
                "tf_endpoint": "http://api.endpoint.com",
            },
            {"show_payload": False},
            "passed",
            {
                "cli": 1,
                "load_configuration": 1,
                "get_board_data": 1,
                "adjust_for_package_testing": 1,
                "determine_tf_compose": 0,
                "generate_payload": 1,
                "to_json_string": 0,
                "make_request_and_wait": 1,
                "post_process_results": 1,
            },
        ),
        (
            {
                "action": "TEST",
                "hw_target": "qdrive3",
                "PACKAGE_NAME": "glibc",
                "tf_endpoint": "http://api.endpoint.com",
            },
            {"show_payload": True},
            "passed",
            {
                "cli": 1,
                "load_configuration": 1,
                "get_board_data": 1,
                "adjust_for_package_testing": 1,
                "determine_tf_compose": 0,
                "generate_payload": 1,
                "to_json_string": 1,
                "make_request_and_wait": 0,
                "post_process_results": 0,
            },
        ),
        (
            {
                "action": "TEST",
                "hw_target": "aws",
                "PACKAGE_NAME": "glibc",
                "tf_endpoint": "http://api.endpoint.com",
            },
            {"show_payload": False},
            "passed",
            {
                "cli": 1,
                "load_configuration": 1,
                "get_board_data": 0,
                "adjust_for_package_testing": 1,
                "determine_tf_compose": 0,
                "generate_payload": 1,
                "to_json_string": 0,
                "make_request_and_wait": 1,
                "post_process_results": 1,
            },
        ),
        (
            {
                "action": "BUILD",
                "hw_target": "aws",
                "build_format": "qcow2",
                "tf_endpoint": "http://api.endpoint.com",
                "tf_compose": "some_compose",
                "IMAGE_KEY": "image_key",
                "arch": "aarch64",
                "stream": "upstream",
            },
            {"show_payload": False},
            "passed",
            {
                "cli": 1,
                "load_configuration": 1,
                "get_board_data": 0,
                "adjust_for_package_testing": 0,
                "determine_tf_compose": 1,
                "generate_payload": 1,
                "to_json_string": 0,
                "make_request_and_wait": 1,
                "post_process_results": 1,
            },
        ),
        (
            {
                "action": "BUILD",
                "hw_target": "qdrive3",
                "build_format": "aboot.simg",
                "tf_endpoint": "http://api.endpoint.com",
                "tf_compose": "some_compose",
                "IMAGE_KEY": "image_key",
                "arch": "aarch64",
                "stream": "upstream",
            },
            {"show_payload": False},
            "passed",
            {
                "cli": 1,
                "load_configuration": 1,
                "get_board_data": 0,
                "adjust_for_package_testing": 0,
                "determine_tf_compose": 1,
                "generate_payload": 1,
                "to_json_string": 0,
                "make_request_and_wait": 1,
                "post_process_results": 1,
            },
        ),
    ],
)
@patch("tf_requests.tf_requests.post_process_results")
@patch("tf_requests.tf_requests.make_request_and_wait")
@patch("tf_requests.tf_requests.to_json_string")
@patch("tf_requests.tf_requests.generate_payload")
@patch("tf_requests.tf_requests.determine_tf_compose")
@patch("tf_requests.tf_requests.adjust_for_package_testing")
@patch("tf_requests.tf_requests.get_board_data")
@patch("tf_requests.tf_requests.load_configuration")
@patch("tf_requests.tf_requests.cli")
@patch("time.sleep", MagicMock())  # patch time.sleep to avoid waiting for WAIT_FOR_SYNC sec in tests
def test_main_flow(
    mock_cli,
    mock_load_configuration,
    mock_get_board_data,
    mock_adjust_for_package_testing,
    mock_determine_tf_compose,
    mock_generate_payload,
    mock_to_json_string,
    mock_make_request_and_wait,
    mock_post_process_results,
    config,
    mock_args,
    test_result,
    expected_calls,
):
    # Mock the script parameters
    args = argparse.Namespace(**mock_args)
    mock_cli.return_value = args
    # Set the test case result
    mock_results["result"]["overall"] = test_result
    mock_make_request_and_wait.return_value = mock_results
    mock_load_configuration.return_value = {}, {}, config
    mock_get_board_data.return_value = "tf_pool", "tf_compose"

    main()

    assert mock_cli.call_count == expected_calls["cli"]
    assert mock_load_configuration.call_count == expected_calls["load_configuration"]
    assert mock_get_board_data.call_count == expected_calls["get_board_data"]
    assert mock_adjust_for_package_testing.call_count == expected_calls["adjust_for_package_testing"]
    assert mock_determine_tf_compose.call_count == expected_calls["determine_tf_compose"]
    assert mock_generate_payload.call_count == expected_calls["generate_payload"]
    assert mock_to_json_string.call_count == expected_calls["to_json_string"]
    assert mock_make_request_and_wait.call_count == expected_calls["make_request_and_wait"]
    assert mock_post_process_results.call_count == expected_calls["post_process_results"]
