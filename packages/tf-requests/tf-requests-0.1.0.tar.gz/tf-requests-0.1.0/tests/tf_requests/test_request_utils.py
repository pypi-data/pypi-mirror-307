from unittest.mock import Mock, patch

import pytest
import requests
import requests_mock
import responses
from responses import registries

from tf_requests.request_utils import (
    display_results,
    download_file,
    get_artifacts_workdir_urls,
    make_request,
    wait_for_job_to_finish,
)

# Parameters: status_code, response_json, expected_result, expected_exception, expected_exception_match
test_data = [
    (200, {"id": "12345", "created": "2020-12-18T20:46:00.392227"}, "12345", None, None),
    (422, {"detail": [{"loc": ["0"], "msg": "Invalid req", "type": "error"}]}, None, ValueError, "Error"),
]


@pytest.mark.parametrize(
    "status_code, response_json, expected_result, expected_exception, expected_exception_match", test_data
)
def test_api_response(status_code, response_json, expected_result, expected_exception, expected_exception_match):
    with requests_mock.Mocker() as m:
        m.post("http://test.com/api", json=response_json, status_code=status_code)
        if expected_exception:
            with pytest.raises(expected_exception, match=expected_exception_match):
                make_request("http://test.com/api", {"key": "value"})
        else:
            result = make_request("http://test.com/api", {"key": "value"})
            assert result == expected_result


def test_non_json_response():
    with requests_mock.Mocker() as m:
        m.post("http://test.com/api", text="Not a JSON", status_code=200)
        with pytest.raises(ValueError, match="Unexpected response from the API"):
            make_request("http://test.com/api", {"key": "value"})


def test_successful_wait_for_job_to_finish_call():
    with requests_mock.Mocker() as m:
        m.get(
            "http://test.com/api/12345",
            json={"id": "12345", "state": "complete"},
            status_code=200,
        )
        result = wait_for_job_to_finish("http://test.com/api", "12345")

        assert "id" in result
        assert result["id"] == "12345"
        assert "state" in result
        assert result["state"] == "complete"


def test_fail_wait_for_job_to_finish_call():
    with requests_mock.Mocker() as m:
        m.get(
            "http://test.com/api/12345",
            json={"id": "12345", "state": "error"},
            status_code=200,
        )
        result = wait_for_job_to_finish("http://test.com/api", "12345")

        assert "id" in result
        assert result["id"] == "12345"
        assert "state" in result
        assert result["state"] == "error"


def test_job_not_found():
    with requests_mock.Mocker() as m:
        m.get(
            "http://test.com/api/12345",
            json={"detail": [{"loc": ["0"], "msg": "Invalid request", "type": "Request not found"}]},
            status_code=422,
        )
        with pytest.raises(ValueError, match="Request not found"):
            wait_for_job_to_finish("http://test.com/api", "12345")


def test_invalid_request():
    with requests_mock.Mocker() as m:
        m.get(
            "http://test.com/api/12345",
            json={"detail": [{"loc": [0], "msg": "Invalid request", "type": "error"}]},
            status_code=422,
        )
        with pytest.raises(ValueError, match="Error"):
            wait_for_job_to_finish("http://test.com/api", "12345")


@pytest.mark.parametrize("code", [422])
def test_wait_for_job_unexpected_error(code):
    with requests_mock.Mocker() as m:
        m.get(
            "http://test.com/api/12345",
            json={"detail": [{"loc": ["0"], "msg": "Invalid request", "type": "Unexpected error"}]},
            status_code=code,
        )
        with pytest.raises(ValueError, match="Unexpected error"):
            wait_for_job_to_finish("http://test.com/api", "12345")


@responses.activate(registry=registries.OrderedRegistry)
def test_wait_for_server_errors():
    # Define multiple responses for requests.get()
    url = "http://test.com/api/12345"
    r1 = responses.get(url, body='{"code": 0, "message": "Bad Gateway"}', status=502)
    r2 = responses.get(url, body='{"id": "12345", "state": "complete"}', status=200)

    result = wait_for_job_to_finish("http://test.com/api", "12345")
    assert result["state"] == "complete"
    assert r1.call_count == 1
    assert r2.call_count == 1


def test_wait_for_job_to_finish_with_retries(mocker):
    # Define multiple responses for requests.get()
    # First response is 'running', second is 'complete'.
    responses = [{"state": "running"}, {"state": "complete"}]

    # Define a side effect function for our mock
    def side_effect(*args, **kwargs):
        return_value = responses.pop(0)
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = return_value
        return mock_response

    # Apply side effect to the mock object
    mocker.patch("requests.Session.get", side_effect=side_effect)
    mocker.patch("time.sleep", return_value=None)

    result = wait_for_job_to_finish("http://test.com/api", "12345")
    assert result["state"] == "complete"


def test_wait_for_job_to_finish_request_exception(mocker):
    # Mock requests.get() to raise a RequestException
    mocker.patch("requests.Session.get", side_effect=requests.exceptions.RequestException("Mocked error"))

    # Attempting to call the function should raise a ValueError with the expected error message
    with pytest.raises(ValueError, match=r"Failed to get job status: Mocked error"):
        wait_for_job_to_finish("http://test.com/api", "12345")


# Test download file
def mock_response(*args, **kwargs):
    mock = Mock()
    mock.iter_content.return_value = iter([b"chunk1", b"chunk2"])
    mock.raise_for_status.return_value = None  # Ensure that raise_for_status does not raise an exception
    return mock


def mock_failure(*args, **kwargs):
    mock = Mock()
    mock.raise_for_status.side_effect = requests.HTTPError()
    return mock


@pytest.mark.parametrize("failures", [0, 1, 2, 3])  # Add 3 to test the case where the max retries is reached
def test_download_file_with_retries(failures):
    with patch("requests.get") as mock_get, patch("time.sleep"):
        mock_get.side_effect = [mock_failure()] * failures + [mock_response()]

        if failures <= 3:  # If we expect the function to eventually succeed
            assert download_file("http://example.com/file", "/tmp/dir/", "report.json")
            assert mock_get.call_count == failures + 1  # Ensure the GET request was called the right number of times
        else:  # If we expect the function to fail after max retries
            with pytest.raises(requests.HTTPError):
                download_file("http://example.com/file", "/tmp/dir/", "report.json")
            assert mock_get.call_count == 3


# Testing results
mock_results = {
    "id": "12345",
    "result": {"overall": "passed"},
    "run": {"artifacts": "http://example.com/report"},
}


def test_display_results():
    with patch("logging.info") as mock_log:
        display_results(mock_results)

        mock_log.assert_any_call("Show info for the job 12345:")
        mock_log.assert_any_call("Test result: passed")
        mock_log.assert_any_call("Testing Farm report: http://example.com/report")

    assert mock_log.call_count == 3


# Define test cases for get_artifacts_workdir_urls()
workdir_test_data = [
    # Normal valid results
    (
        {
            "result": {
                "xunit_url": "http://example.com/xunit.xml",
                # Keep the xunit content for mocking the response
                "xunit": "<testsuites><testsuite name='/acl/plans/tests'><logs>"
                '<log name="workdir" href="http://desired_url.com"></log>'
                '<log name="other" href="http://not_the_desired_url.com"></log>'
                "</logs></testsuite></testsuites>",
            }
        },
        # expected output
        [{"name": "/acl/plans/tests", "workdir": "http://desired_url.com"}],
    ),
    # Single log valid results
    (
        {
            "result": {
                "xunit_url": "http://example.com/xunit.xml",
                # Keep the xunit content for mocking the response
                "xunit": "<testsuites><testsuite name='/acl/plans/tests'><logs>"
                '<log name="workdir" href="http://desired_url.com"></log>'
                "</logs></testsuite></testsuites>",
            }
        },
        [{"name": "/acl/plans/tests", "workdir": "http://desired_url.com"}],
    ),
    # Missing xunit
    (
        {"result": {}},
        # expected output
        [],
    ),
    # Invalid XML
    (
        {
            "result": {
                "xunit_url": "http://example.com/xunit.xml",
                # Keep the xunit content for mocking the response
                "xunit": "<testsuites><testsuite name='/acl/plans/tests'><logs>"
                '<log name="workdir" href="http://desired_url.com">'  # Missing closing tag for <log>
                "</logs></testsuite></testsuites>",
            }
        },
        # expected output
        [],
    ),
    # Missing desired URL with multiple logs
    (
        {
            "result": {
                "xunit_url": "http://example.com/xunit.xml",
                # Keep the xunit content for mocking the response
                "xunit": "<testsuites><testsuite name='/acl/plans/tests'><logs>"
                '<log name="something" href="http://not_the_desired_url.com"></log>'  # Missing 'workdir' log
                '<log name="other" href="http://not_the_desired_url.com"></log>'  # Missing 'workdir' log
                "</logs></testsuite></testsuites>",
            }
        },
        # expected output
        [],
    ),
    # Single log missing desired URL
    (
        {
            "result": {
                "xunit_url": "http://example.com/xunit.xml",
                # Keep the xunit content for mocking the response
                "xunit": "<testsuites><testsuite name='/'acl/plans/tests'><logs>"
                '<log name="other" href="http://not_the_desired_url.com"></log>'  # Missing 'workdir' log
                "</logs></testsuite></testsuites>",
            }
        },
        # expected output
        [],
    ),
    # multiple testsuites
    (
        {
            "result": {
                "xunit_url": "http://example.com/xunit.xml",
                # Keep the xunit content for mocking the response
                "xunit": """
<testsuites overall-result="failed">
    <testsuite name="/glibc/plans/tests/fusa/malloc" result="failed" tests="1">
    <logs>
    <log href="http://artifacts.osci.redhat.com/testing-farm/4c41ee2b-a76e-44b3-abf6-783414dbbb2e/work-mallocu07wsv07"
    name="workdir"/>
    </logs>
    </testsuite>
    <testsuite name="/glibc/plans/tests/fusa/math" result="failed" tests="1">
    <logs>
    <log href="http://artifacts.osci.redhat.com/testing-farm/4c41ee2b-a76e-44b3-abf6-783414dbbb2e/work-mathmnfk0w2k"
    name="workdir"/>
    </logs>
    </testsuite>
</testsuites>
                """,
            }
        },
        # expected output
        [
            {
                "name": "/glibc/plans/tests/fusa/malloc",
                "workdir": "http://artifacts.osci.redhat.com/testing-farm/"
                "4c41ee2b-a76e-44b3-abf6-783414dbbb2e/work-mallocu07wsv07",
            },
            {
                "name": "/glibc/plans/tests/fusa/math",
                "workdir": "http://artifacts.osci.redhat.com/testing-farm/"
                "4c41ee2b-a76e-44b3-abf6-783414dbbb2e/work-mathmnfk0w2k",
            },
        ],
    ),
]


@pytest.mark.parametrize("results, expected_url", workdir_test_data)
def test_get_artifacts_workdir_urls(results, expected_url):
    # Mock the HTTP request
    with requests_mock.Mocker() as m:
        # If there's a xunit_url in the results, mock the response
        xunit_url = results.get("result", {}).get("xunit_url")
        if xunit_url:
            # Get the XML content from the original test data
            xml_content = results.get("result", {}).get("xunit", "")
            m.get(xunit_url, text=xml_content)
        assert get_artifacts_workdir_urls(results) == expected_url
