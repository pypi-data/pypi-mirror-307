import os

import pytest

from tf_requests.env_utils import sanitize_job_name, segregate_env_vars


def setup_function():
    # Clear os.environ before each test
    os.environ.clear()


def test_known_transformations():
    os.environ["TF_ENDPOINT"] = "https//api.testing-farm.io/"
    os.environ["TF_API_KEY"] = "1234"
    os.environ["CI_REPO_URL"] = "http://example.com"
    os.environ["CI_REF"] = "my_branch"
    os.environ["TMT_PLAN"] = "my_plan"
    os.environ["ARCH"] = "x86_64"
    os.environ["IMAGE_KEY"] = "key"
    os.environ["TF_COMPOSE"] = "compose"
    os.environ["WEBSERVER_RELEASES"] = "http://webserver.com/releases"

    secrets_env, variables_env, config_env = segregate_env_vars([], [])

    assert config_env["tf_endpoint"] == "https//api.testing-farm.io/"
    assert config_env["api_key"] == "1234"
    assert config_env["test__fmf__url"] == "http://example.com"
    assert config_env["test__fmf__ref"] == "my_branch"
    assert config_env["test__fmf__name"] == "my_plan"


def test_meta_var_extraction():
    os.environ["META_VARIABLE"] = '{"new_var_1": "some value 1", "new_var_2": "some value 2"}'
    os.environ["META_SECRETS"] = '{"secret": "password"}'
    os.environ["META_CONTEXT"] = '{"os": "centos"}'
    os.environ["META_ENVIRONMENT"] = '{"POLARION_USERNAME":"polarion"}'
    os.environ["TF_ENDPOINT"] = "https//api.testing-farm.io/"
    os.environ["TF_API_KEY"] = "1234"
    os.environ["ARCH"] = "x86_64"
    os.environ["IMAGE_KEY"] = "key"
    os.environ["TF_COMPOSE"] = "compose"
    os.environ["CI_REPO_URL"] = "http://example.com"
    os.environ["WEBSERVER_RELEASES"] = "http://webserver.com/releases"

    secrets_env, variables_env, config_env = segregate_env_vars([], [])

    assert variables_env["new_var_1"] == "some value 1"
    assert variables_env["new_var_2"] == "some value 2"
    assert secrets_env["secret"] == "password"
    assert config_env["environments__tmt__context__os"] == "centos"
    assert config_env["environments__tmt__environment__POLARION_USERNAME"] == "polarion"


@pytest.mark.parametrize(
    "os_environ, expected_msg",
    [
        # Testing required image keys
        ({"TF_API_KEY": "1234"}, "Missing keys: ARCH, IMAGE_KEY, TF_COMPOSE, CI_REPO_URL"),
        # Testing required pkgs keys
        ({"TF_API_KEY": "1234", "ACTION": "TEST", "PACKAGE_NAME": "glibc"}, "Missing keys: ARCH, WEBSERVER_RELEASES"),
    ],
)
def test_missing_required_images_keys(os_environ, expected_msg):
    for key, value in os_environ.items():
        os.environ[key] = value

    with pytest.raises(ValueError, match=rf"{expected_msg}"):
        segregate_env_vars([], [])


def test_proper_segregation():
    os.environ["TF_ENDPOINT"] = "https//api.testing-farm.io/"
    os.environ["SECRET_KEY"] = "secret_value"
    os.environ["KNOWN_VAR"] = "var_value"
    os.environ["TF_API_KEY"] = "1234"
    os.environ["CI_REPO_URL"] = "http://example.com"
    os.environ["ARCH"] = "x86_64"
    os.environ["IMAGE_KEY"] = "key"
    os.environ["TF_COMPOSE"] = "compose"
    os.environ["WEBSERVER_RELEASES"] = "http://webserver.com/releases"
    os.environ["environments__variables__new_var"] = "some_value"

    secrets_env, variables_env, config_env = segregate_env_vars(["SECRET_KEY"], ["KNOWN_VAR"])

    assert "SECRET_KEY" not in variables_env
    assert "SECRET_KEY" not in config_env
    assert secrets_env["SECRET_KEY"] == "secret_value"
    assert variables_env["KNOWN_VAR"] == "var_value"
    assert config_env["KNOWN_VAR"] == "var_value"
    assert config_env["api_key"] == "1234"
    assert config_env["environments__variables__new_var"] == "some_value"


# Test cases for CI_JOB_NAMEs to sanitize
test_cases = [
    ("smoke-tests-minimal: [aarch64]", "smoke-tests-minimal:aarch64"),
    ("package-test-non-coverage: [qa]", "package-test-non-coverage:qa"),
    ("kernel-test-non-coverage: [sst_kernel_ft, qa]", "kernel-test-non-coverage:sst_kernel_ft,qa"),
    ("/plans/test-case: [x86]", "test-case:x86"),
    ("example-job: [extra_info]", "example-job:extra_info"),
]


@pytest.mark.parametrize("input_name, expected", test_cases)
def test_sanitize_job_name(input_name, expected):
    assert sanitize_job_name(input_name) == expected
