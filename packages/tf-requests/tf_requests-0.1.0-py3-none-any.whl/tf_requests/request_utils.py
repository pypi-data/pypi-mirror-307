#!/usr/bin/env python3

"""
request_utils: Utility functions for interacting with the Testing Farm API.

This module provides a collection of utility functions designed to facilitate interactions with
the Testing Farm API.
The functionalities include making POST requests to specified endpoints, polling job status,
fetching job results, displaying said results, and downloading files from given URLs.

Key Functions:
- make_request: Send a POST request to a given API endpoint.
- wait_for_job_to_finish: Continuously poll the API until a job completes. Then fetch response from the API
  and return the results from the TF job.
- display_results: Display the job results.
- download_file: Download files from specified URLs with retry capability.

Note:
    This module is designed for use within CI/CD pipelines, especially in GitLab, and relies on
    appropriate environment variables being set for its operations.
"""


import logging
import os
import time
from typing import Any, Dict, Optional

import requests
import xmltodict
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util import Retry

from .payload_utils import to_json_string

API_SUCCESS_CODES = [200, 201]

MAX_RETRIES = 5
TIMEOUT = 10
DELAY = 5

HEADER_NO_CACHE = {"Cache-Control": "no-cache"}


def make_request(endpoint: str, payload: Dict[str, Any]) -> Optional[str]:
    """
    Make a POST request to the specified endpoint with the provided payload.

    Args:
        endpoint (str): The API endpoint to which the request is to be made.
        payload (Dict[str, Any]): The payload to be sent in the POST request.

    Returns:
        Optional[str]: The job ID if the request is successful; otherwise,
        raises a ValueError with an appropriate error message.
    """
    response = requests.post(endpoint, json=payload)
    error_message = ""
    # If the response contains a message, append it to the error message
    try:
        response_data = response.json()
        # Check for HTTP status codes and handle accordingly
        if response.status_code in API_SUCCESS_CODES:
            job_id = response_data.get("id")
            logging.info(f"Request successful. Job id: '{job_id}'")
            return job_id

        if "detail" in response_data:
            error_message += f"\nError Message: {response_data['detail'][0]['msg']}"
            error_message += f"\nError Type: {response_data['detail'][0]['type']}"
            error_message += f"\nError Location: {response_data['detail'][0]['loc']}"
    except requests.exceptions.Timeout:
        raise ValueError("Request timeout occured.")
    except requests.exceptions.TooManyRedirects:
        raise ValueError("Too many redirects occurred. The URL may be bad. Please try a different URL.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Unexpected response from the API: {e}")
    raise ValueError(error_message)


def wait_for_job_to_finish(tf_endpoint: str, job_id: str) -> Dict[str, Any]:
    """
    Poll the status of a specific job until it finishes.

    Args:
        tf_endpoint (str): The base Testing Farm API endpoint.
        job_id (str): The ID of the job to monitor.

    Returns:
        Dict[str, Any]: The results of the finished job.
    """
    logging.info(f"Wait for the job '{job_id}' to finish")
    logging.info(f"Runnig at: {tf_endpoint}/{job_id}")

    # Define retry strategy
    retry_strategy = Retry(backoff_factor=DELAY, status_forcelist=[500, 502, 503, 504])

    # Create an HTTP adapter with the retry strategy and mount it to session
    adapter = HTTPAdapter(max_retries=retry_strategy)

    # Create a new session object
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    status = ""
    error_message = ""
    while True:
        try:
            response = session.get(f"{tf_endpoint}/{job_id}")
            response_json = response.json()

            if response.status_code in API_SUCCESS_CODES:
                status = response_json["state"]
            else:
                if "detail" in response_json:
                    error_message += f"\nError Message: {response_json['detail'][0]['msg']}"
                    error_message += f"\nError Type: {response_json['detail'][0]['type']}"
                    error_message += f"\nError Location: {response_json['detail'][0]['loc']}"
                raise ValueError(error_message)

            if status in ["complete", "error"]:
                break
            time.sleep(30)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get job status: {e}")

    logging.debug(to_json_string(response_json))
    return response_json


def display_results(results: Dict[str, Any]) -> None:
    """
    Display the results of a specific job.

    Args:
        results (Dict[str, Any]): The results of the job to display.
    """
    job_id = results["id"]
    result = results["result"]["overall"]
    report_url = results["run"]["artifacts"]

    logging.info(f"Show info for the job {job_id}:")
    logging.info(f"Test result: {result}")
    logging.info(f"Testing Farm report: {report_url}")


def download_file(url: str, destination: str, filename: str, delay: int = DELAY) -> bool:
    """
    Download a file from a given URL and save it to a specified location.

    Args:
        url (str): The URL of the file to download.
        destination (str): The directory to save the downloaded file.
        filename (str): The name to save the file as.

    Returns:
        bool: True if the download was successful, False otherwise.
    """
    # Make sure the target directory exist before downloading the report
    if not os.path.exists(destination):
        os.makedirs(destination, exist_ok=True)
    file_full_path = f"{destination}/{filename}"
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url, timeout=TIMEOUT, verify=False, headers=HEADER_NO_CACHE)
            response.raise_for_status()
            with open(file_full_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return True
        except (requests.HTTPError, RequestException) as e:
            # This will handle any kind of exception related to the request like
            # http errors, connection errors, timeouts, etc.
            # The download is retries multiple times given this type of error
            if retries >= MAX_RETRIES:
                logging.error(f"Error downloading the file from {url} ({retries} attempts made). Error: {e}")
                raise  # Re-raise the exception if max retries are reached
            retries += 1
            time.sleep(delay)
        except IOError as e:
            # Handle any file-related errors here
            logging.error(f"File operation error: {e}")
            raise

    return False


def get_artifacts_workdir_urls(results: Dict[str, Any]) -> list[Dict[str, str]]:
    """
    Extract the artifacts workdir URLs from the XML embedded into the request response.

    Args:
        results (Dict[str, Any]): The results of the finished job.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing the testsuite name and its workdir URL.
    """
    workdir_urls = []  # type: ignore
    try:
        # Get the URL for the XML file
        xunit_url = results.get("result", {}).get("xunit_url")
        if not xunit_url:
            logging.error("No xunit_url found in results.")

        # Download XML content
        try:
            response = requests.get(xunit_url, timeout=TIMEOUT, verify=False, headers=HEADER_NO_CACHE)
            response.raise_for_status()
            xunit = response.text
        except requests.RequestException as e:
            logging.error(f"Failed to download XML from {xunit_url}: {e}")
            return workdir_urls

        # Process XML content
        xunit_dict = xmltodict.parse(xunit)
        testsuites = xunit_dict.get("testsuites", {}).get("testsuite", [])
        if not isinstance(testsuites, list):
            testsuites = [testsuites]

        for testsuite in testsuites:
            logs = testsuite.get("logs", {}).get("log", [])
            if not isinstance(logs, list):
                logs = [logs]

            workdir_url = None
            testsuite_name = testsuite["@name"]

            for log in logs:
                if log.get("@name") == "workdir":
                    workdir_url = log["@href"]
                    break

            if workdir_url:
                workdir_urls.append({"name": testsuite_name, "workdir": workdir_url})

        if not workdir_urls:
            logging.error("No artifacts workdir URLs were found")
        return workdir_urls

    except Exception as e:
        logging.error(f"Error while extracting workdir URLs: {e}")
        return []
