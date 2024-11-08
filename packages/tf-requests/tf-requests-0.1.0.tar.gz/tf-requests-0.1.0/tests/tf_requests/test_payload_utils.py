import json
import re

import pytest

from tf_requests.payload_utils import (
    _validate_payload,
    create_initial_payload,
    to_json_string,
    update_from_path,
)


def test_to_json_string():
    data = {"key": "value"}
    json_string = to_json_string(data)

    assert type(json_string) is str
    try:
        json.loads(json_string)
    except json.JSONDecodeError:
        assert False, "Output is not a valid JSON"
    assert True


test_cases = [
    (
        "fake_apikey",
        "http://fake-url.com/repo.git",
        "x86_64",
        "fake_pool",
        "centos_stream_9",
        {
            "api_key": "fake_apikey",
            "test": {
                "fmf": {
                    "url": "http://fake-url.com/repo.git",
                    "ref": "main",
                    "name": "",
                }
            },
            "environments": [
                {
                    "arch": "x86_64",
                    "os": {"compose": "centos_stream_9"},
                    "pool": "fake_pool",
                    "tmt": {"context": {}, "environment": {}},
                    "variables": {},
                    "secrets": {},
                }
            ],
        },
    ),
    (
        "fake_apikey2",
        "http://fake-url.com/repo.git",
        "aarch64",
        "",
        "rhel9",
        {
            "api_key": "fake_apikey2",
            "test": {"fmf": {"url": "http://fake-url.com/repo.git", "ref": "main", "name": ""}},
            "environments": [
                {
                    "arch": "aarch64",
                    "os": {"compose": "rhel9"},
                    "pool": "",
                    "tmt": {"context": {}, "environment": {}},
                    "variables": {},
                    "secrets": {},
                }
            ],
        },
    ),
]


@pytest.mark.parametrize(
    "api_key, git_url, arch, pool, compose, expected",
    test_cases,
)
def test_payload_is_valid_json(
    api_key,
    git_url,
    arch,
    pool,
    compose,
    expected,
):
    result = create_initial_payload(
        api_key,
        git_url,
        arch,
        pool,
        compose,
    )
    try:
        json.dumps(result)
    except json.JSONDecodeError:
        assert False, "Output is not a valid JSON"
    assert True


@pytest.mark.parametrize(
    "api_key, git_url, arch, pool, compose, expected",
    test_cases,
)
def test_has_mandatory_keys(
    api_key,
    git_url,
    arch,
    pool,
    compose,
    expected,
):
    result = create_initial_payload(
        api_key,
        git_url,
        arch,
        pool,
        compose,
    )
    assert "api_key" in result
    assert "url" in result["test"]["fmf"]
    assert "ref" in result["test"]["fmf"]
    assert "name" in result["test"]["fmf"]
    assert "arch" in result["environments"][0]
    assert "pool" in result["environments"][0]
    assert "compose" in result["environments"][0]["os"]
    assert "context" in result["environments"][0]["tmt"]
    assert "environment" in result["environments"][0]["tmt"]
    assert "variables" in result["environments"][0]
    assert "secrets" in result["environments"][0]


@pytest.mark.parametrize(
    "api_key, git_url, arch, pool, compose, expected",
    test_cases,
)
def test_valid_object_keys(
    api_key,
    git_url,
    arch,
    pool,
    compose,
    expected,
):
    result = create_initial_payload(
        api_key,
        git_url,
        arch,
        pool,
        compose,
    )
    assert isinstance(result["api_key"], str)
    assert isinstance(result["test"]["fmf"]["url"], str)
    assert isinstance(result["test"]["fmf"]["ref"], str)
    assert isinstance(result["test"]["fmf"]["name"], str)
    assert isinstance(result["environments"][0]["arch"], str)
    assert isinstance(result["environments"][0]["pool"], str)
    assert isinstance(result["environments"][0]["os"]["compose"], str)
    assert isinstance(result["environments"][0]["tmt"]["context"], dict)
    assert isinstance(result["environments"][0]["tmt"]["environment"], dict)
    assert isinstance(result["environments"][0]["variables"], dict)
    assert isinstance(result["environments"][0]["secrets"], dict)


@pytest.mark.parametrize(
    "api_key, git_url, arch, pool, compose, expected",
    test_cases,
)
def test_pass_the_righ_data(
    api_key,
    git_url,
    arch,
    pool,
    compose,
    expected,
):
    result = create_initial_payload(
        api_key,
        git_url,
        arch,
        pool,
        compose,
    )
    assert result == expected


@pytest.mark.parametrize(
    "payload, expected_error_message",
    [
        (
            {
                "api_key": "",
                "test": {
                    "fmf": {
                        "url": "http://fake-url.com/repo.git",
                    }
                },
                "environments": [
                    {
                        "arch": "x86_64",
                        "os": {"compose": "centos_stream_9"},
                    }
                ],
            },
            "The 'api_key' parameter is required and cannot be an empty string.",
        ),
        (
            {
                "api_key": None,
                "test": {
                    "fmf": {
                        "url": "http://fake-url.com/repo.git",
                    }
                },
                "environments": [
                    {
                        "arch": "x86_64",
                        "os": {"compose": "centos_stream_9"},
                    }
                ],
            },
            "The 'api_key' parameter is required and cannot be an empty string.",
        ),
        (
            {
                "test": {
                    "fmf": {
                        "url": "http://fake-url.com/repo.git",
                    }
                },
                "environments": [
                    {
                        "arch": "x86_64",
                        "os": {"compose": "centos_stream_9"},
                    }
                ],
            },
            "The 'api_key' parameter is required and cannot be an empty string.",
        ),
        (
            {
                "api_key": "fake_api_key",
                "test": {
                    "fmf": {
                        "url": "",
                    }
                },
                "environments": [
                    {
                        "arch": "x86_64",
                        "os": {"compose": "centos_stream_9"},
                    }
                ],
            },
            "The 'test.fmf.url' parameter is required and cannot be an empty string.",
        ),
        (
            {
                "api_key": "fake_api_key",
                "test": {
                    "fmf": {
                        "url": None,
                    }
                },
                "environments": [
                    {
                        "arch": "x86_64",
                        "os": {"compose": "centos_stream_9"},
                    }
                ],
            },
            "The 'test.fmf.url' parameter is required and cannot be an empty string.",
        ),
        (
            {
                "api_key": "fake_api_key",
                "test": {},
                "environments": [
                    {
                        "arch": "x86_64",
                        "os": {"compose": "centos_stream_9"},
                    }
                ],
            },
            "The 'test.fmf' parameter is required and cannot be an empty dict.",
        ),
        (
            {
                "api_key": "fake_api_key",
                "test": {
                    "fmf": {
                        "url": "http://fake-url.com/repo.git",
                    }
                },
                "environments": [
                    {
                        "arch": "",
                        "os": {"compose": "centos_stream_9"},
                    }
                ],
            },
            "The 'environments[0].arch' parameter is required and cannot be an empty string.",
        ),
        (
            {
                "api_key": "fake_api_key",
                "test": {
                    "fmf": {
                        "url": "http://fake-url.com/repo.git",
                    }
                },
                "environments": [
                    {
                        "arch": "aarch64",
                        "os": {"compose": ""},
                    }
                ],
            },
            "The 'environments[0].os.compose' parameter is required and cannot be an empty string.",
        ),
    ],
)
def test_missing_or_empty_parameters(payload, expected_error_message):
    with pytest.raises(ValueError, match=re.escape(expected_error_message)):
        _validate_payload(payload)


@pytest.mark.parametrize(
    "dictionary_path, update_data, check_path, check_key, expected_value",
    [
        (
            "environments__variables",
            {"VAR1": "value1", "VAR2": "value2"},
            "environments[0].variables",  # Equivalent to ["environments"][0]["variables"]
            "VAR1",
            "value1",
        ),
        (
            "environments__secrets",
            {"secret": "somesecret", "password": "superpassword"},
            "environments[0].secrets",
            "password",
            "superpassword",
        ),
        ("environments__newkey", "some_value", "environments[0]", "newkey", "some_value"),
        ("environments__tmt__context__newkey", "some_value", "environments[0].tmt.context", "newkey", "some_value"),
        ("test__fmf__newkey", "some_value", "test.fmf", "newkey", "some_value"),
    ],
)
def test_update_from_path(dictionary_path, update_data, check_path, check_key, expected_value):
    payload = create_initial_payload(
        "api_key", "http://example.com/repo.git", "aarch64", "centosstream9", "CentOS Stream 9"
    )
    update_from_path(payload, dictionary_path, update_data)

    # Move the 'payload' dictionary to the level from the 'check_path'
    # So, with a 'check_path' like this 'environments[0].variables', payload become:
    # payload["environments"][0]["variables"].
    # And with 'check_path' equal to 'test.fmf':
    # payload = payload["test"]["fmf"]
    for part in check_path.split("."):
        if part == "environments[0]":
            payload = payload["environments"][0]
        else:
            payload = payload[part]

    assert check_key in payload  # Check that the key exist at that level
    assert payload[check_key] == expected_value  # Check the velue for that key is the expected one
