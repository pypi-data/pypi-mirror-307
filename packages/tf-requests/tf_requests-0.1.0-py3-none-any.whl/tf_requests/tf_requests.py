#!/usr/bin/env python3

"""
This module facilitates calls to an external API for running builds and tests.
Designed primarily for use within GitLab CI/CD jobs, it leverages environment variables and secrets
to compose and send requests.

Functionalities:
- Load configuration from environment variables.
- Generate a payload based on the configuration, variables, and secrets.
- Make a POST request to the specified API endpoint with the generated payload.
- Wait for the job associated with the request to complete.
- Retrieve and display the results of the job.
- Optionally, store the results for future reference.
- Save environment variables post-job completion.
- Handle errors and failures based on predefined error codes.

Usage:
    Set the required environment variables (see README.md for a sample).
    Then execute the script:
        $ pdm run tf_requests [--variables VARIABLES] [--secrets SECRETS] [--show-payload]

CLI Arguments:
    --variables VARIABLES   Path to a JSON file containing variables.
    --secrets SECRETS       Path to a JSON file containing secrets.
    --show-payload          Display the generated payload without making an actual request.

Note:
    Proper logging is implemented, and the verbosity can be controlled via the LOGLEVEL environment variable.
"""
import argparse
import json
import logging
import os
import sys
from http.client import HTTPConnection
from typing import Any, Dict, Tuple

from .data_utils import (
    determine_board_base_url,
    determine_tf_compose,
    generate_board_compose,
    get_package_nvr,
    populate_board_variables,
)
from .env_utils import sanitize_job_name, segregate_env_vars
from .get_auto_compose import calculate_auto_compose
from .payload_utils import create_initial_payload, to_json_string, update_from_path
from .request_utils import (
    display_results,
    download_file,
    get_artifacts_workdir_urls,
    make_request,
    wait_for_job_to_finish,
)

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
if LOGLEVEL == "DEBUG":
    # Enable HTTP low level debug
    HTTPConnection.debuglevel = 1

TESTS_RESULTS_DIR = "tests_results"
RESULTS_JUNIT_FILE = "results-junit.xml"
ENV_VARS_FILE = "pipeline.env"

TF_DEFAULT_ENDPOINT = "https://api.dev.testing-farm.io/v0.1/requests"
UPSTREAM_WEBSERVR_RELEASE = "https://autosd.sig.centos.org/AutoSD-9"
# We consider those results code to be a Testing Farm or tmt issue, not a test fail
TF_ERRORS = ["error", "unknown", "skipped"]
TEST_VALID_CODES = ["passed", "failed"]
TEST_ERROR_CODES = ["error", "unknown", "skipped"]

DISK_SIZE_BUILD = ">= 25 GB"


def cli() -> argparse.Namespace:
    """
    CLI function to parse arguments.
    """
    parser = argparse.ArgumentParser(description="TF Requests tool")
    parser.add_argument("--variables", type=str, help="A comma-separated list of variable names")
    parser.add_argument("--secrets", type=str, help="A comma-separated list of secret names")
    parser.add_argument("--show-payload", action="store_true", help="Only generate and show the payload")
    args = parser.parse_args()
    return args


def load_configuration(
    args: argparse.Namespace,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """
    Load configuration from environment variables and segregate into secrets, variables, and config.

    Then make sure that all the basic config items have some value. If not, set the default value for them.

    Args:
        args (argparse.Namespace): Arguments passed to the cli.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]: Three dictionaries from the segretate data from
        the ENV variables:
        - secrets: variables to be passed as variables to TF via tmt.
        - variables: variables to be passed as secrets to TF via tmt.
        - config: variables to be used in different operations by the program.
    """
    variables_list = []
    secrets_list = []

    if args.variables:
        variables_list = [var.strip() for var in args.variables.split(",")]

    if args.secrets:
        secrets_list = [secret.strip() for secret in args.secrets.split(",")]

    # Create the different list of variables from teh ENV variables
    secrets, variables, config = segregate_env_vars(secrets_list, variables_list)

    # Define some basic variables and set some defaults values
    config["tf_endpoint"] = config.get("tf_enpoint", TF_DEFAULT_ENDPOINT)
    config["webserver_releases"] = config.get("WEBSERVER_RELEASES", UPSTREAM_WEBSERVR_RELEASE)
    config["arch"] = config["environments__arch"]
    config["build_format"] = config.get("BUILD_FORMAT", "qcow2")
    config["hw_target"] = config.get("HW_TARGET", "aws")
    config["upload_prefix"] = config.get("S3_UPLOAD_PREFIX", "sample-images")
    config["release_name"] = variables.get("RELEASE_NAME", None)
    config["x_stream"] = variables.get("X_STREAM", None)
    if config["x_stream"]:
        config["webserver_releases"] = f"{config['webserver_releases']}/{config['x_stream']}"
    # There is a TF_POOL defined per arch (TF_POOL_x86_64 and TF_POOL_aarch64),
    # we need to use the one for the current arch
    config["tf_pool"] = config.get(f"TF_POOL_{config['arch']}", "")
    config["action"] = config.get("ACTION", "BUILD")
    config["stream"] = config.get("STREAM", "UPSTREAM")

    config["tf_compose"] = config.get("TF_COMPOSE", "CentOS-Stream-9")

    return secrets, variables, config


def get_board_data(config: Dict[str, Any]) -> Tuple[str, str]:
    """
    Calculated the right tf_pool and generate the tf_compose for a board test jobs.

    Args:
        config (Dict[str, Any]): Dictionary with the program configuration.

    Returns:
        Tuple[str, str]: The calculated values for 'tf_pool' and 'tf_compose'
    """
    hw_target = config["hw_target"]
    logging.debug(f"Generating compose for board '{hw_target}'. ACTION=TEST")
    if "webserver_releases" not in config:
        raise ValueError("'WEBSERVER_RELEASES' can't be empty for a board tests")

    upload_prefix, tf_pool = populate_board_variables(
        config["upload_prefix"], config["tf_pool"], config["arch"], hw_target
    )
    base_url = determine_board_base_url(
        config["release_name"],
        config.get("WEBSERVER_WORKSPACES", ""),  # It won't exist for pkg testing
        config["WORKSPACE_ID"],
        upload_prefix,
        config["IMAGE_KEY"],
        config["webserver_releases"],
    )
    tf_compose = generate_board_compose(base_url=base_url, hw_target=hw_target)

    return tf_pool, tf_compose


def adjust_for_package_testing(config: Dict[str, Any], variables: Dict[str, Any]) -> None:
    """
    Update config and variables dictionaries with the necessary changes for testing packages

    Args:
        config (Dict[str, Any]): Variables to be used in different operations by the program.
        variables (Dict[str, Any]): Variables to be passed as secrets to TF via tmt.
    """
    logging.info(f"Running the package testing for the package '{config['PACKAGE_NAME']}'")
    if "RELEASE_NAME" not in config or not config["RELEASE_NAME"]:
        config["RELEASE_NAME"] = "nightly"

    if "PACKAGE_NVR" not in config:
        try:
            config["PACKAGE_NVR"] = get_package_nvr(config, config["PACKAGE_NAME"])
        except ValueError as e:
            raise ValueError(e)

    variables["PACKAGE_NVR"] = config["PACKAGE_NVR"]
    logging.info(f"Package NVR: {config['PACKAGE_NVR']}")

    calculated = calculate_auto_compose(config)
    variables["IMAGE_KEY"] = config["IMAGE_KEY"]
    logging.info(f"IMAGE_KEY: {config['IMAGE_KEY']}")
    if not calculated:
        raise ValueError("ERROR: Something was wrong while trying to fetch the information for the image")

    config["tf_pool"], config["tf_compose"] = calculated


def set_boards_settings(config: Dict[str, Any]) -> None:
    """
    Update config and variables dictionaries with the necessary changes for testing on the reference boards.
    The reference boards are all HW_TARGET that is not 'aws', like 'qdrive3' or 'ridesx4'.

    Args:
        config (Dict[str, Any]): Variables to be used in different operations by the program.
    """
    logging.info(f"Running the test on board '{config['hw_target']}'")
    config["tf_pool"], config["tf_compose"] = get_board_data(config)


def generate_payload(config: Dict[str, Any], variables: Dict[str, Any], secrets: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate the payload to make the TF API call.

    Args:
        config (Dict[str, Any]): Variables to be used in different operations by the program.
        variables (Dict[str, Any]): Variables to be passed as secrets to TF via tmt.
        secrets (Dict[str, Any]): Variables to be passed as variables to TF via tmt.

    Returns:
        Dict[str, Any]: Payload for making the API call.
    """
    logging.info("Generating the payload for the Testing Farm request.")
    # Create initial payload from base structure
    payload = create_initial_payload(
        config["api_key"],
        config["test__fmf__url"],
        config["arch"],
        config["tf_pool"],
        config["tf_compose"],
    )

    # Populate variables and secrets
    update_from_path(payload, "environments__variables", variables)
    update_from_path(payload, "environments__secrets", secrets)

    # Add some useful tmt context variables: arch, hw_target, image_type and image_name
    # It allows better filters for the tmt plans and tests.
    config["environments__tmt__context__arch"] = config["arch"]
    config["environments__tmt__context__hw_target"] = config["hw_target"]
    config["environments__tmt__context__image_type"] = config["IMAGE_TYPE"]
    config["environments__tmt__context__image_name"] = config["IMAGE_NAME"]

    # Add the TMT_SCRIPTS_DIR env variable to be able to run tmt scripts like tmt-reboot
    config["environments__tmt__environment__TMT_SCRIPTS_DIR"] = "/usr/local/bin"

    # Add any sub-elements under 'environments[0] or settings' passed as path based variable
    # It includes the 'environments[0].tmt.context' variables.
    for key in config.keys():
        if key.startswith("environments__") or key.startswith("settings__"):
            update_from_path(payload, key, config[key])

    # Add any sub-elements under 'tests' passed as path based variable
    for key in config.keys():
        if key.startswith("test__"):
            update_from_path(payload, key, config[key])

    logging.info("Payload generated.")
    logging.debug(to_json_string(payload))
    return payload


def make_request_and_wait(tf_endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make the API request and wait until the TF job is done or failed. Then, return the response.

    Args:
        tf_endpoint (type): Testing Farm API endpoint for creating new requests or query the results.
        payload (type): JSON like structure for making the API request.

    Returns:
        Dict[str, Any]: The structure with the response from the API.
    """
    try:
        logging.info("Making the Testing Farm request.")
        job_id = make_request(tf_endpoint, payload)
    except ValueError as e:
        logging.error(f"Failure in tf request with the payload:\n{to_json_string(payload)}")
        raise ValueError(e)

    if job_id is None:
        raise ValueError("job_id cannot be None!")

    try:
        response = wait_for_job_to_finish(tf_endpoint, job_id)
    except ValueError as e:
        raise ValueError(e)

    return response


def store_results(results: Dict[str, Any]) -> None:
    """
    Download and store the JUnit file with the results from the TF job.

    Args:
        results (Dict[str, Any]): The structure with the response from the API.
    """
    if results["result"]["overall"] not in TEST_VALID_CODES:
        logging.error("As the job failed, there is no test report to download")
        return

    original_job_name = os.environ.get("CI_JOB_NAME", "test")
    job_name = sanitize_job_name(original_job_name)
    artifacts_url = results["run"]["artifacts"]

    report_url = f"{artifacts_url}/{RESULTS_JUNIT_FILE}"
    report_filename = f"{job_name}-{RESULTS_JUNIT_FILE}"
    report_path = f"{TESTS_RESULTS_DIR}/{report_filename}"

    logging.info(f"Downloading the JUnit xml file from: {report_url}")
    if download_file(report_url, TESTS_RESULTS_DIR, report_filename, delay=60):
        logging.info(f"The JUnit xml file was successfully stored at '{report_path}'")
    else:
        logging.error("There was an error and the report file wasn't stored locally")


def save_env_vars(results: Dict[str, Any], config: Dict[str, Any]) -> None:
    """
    Save some ENV variables into a file to be used outside this script

    Args:
        results (Dict[str, Any]): The structure with the response from the API.
        config (Dict[str, Any]): Variables to be used in different operations by the program.
    """
    env_vars = {
        "ARTIFACTS_URL": results["run"]["artifacts"],
        "ARTIFACTS_WORKDIR_URLS": config.get("artifacts_workdir_urls", ""),
        "RESULT": results["result"]["overall"],
        "RELEASE_NAME": config.get("release_name", ""),  # Not set for product pipelines
        "IMAGE_NAME": config["IMAGE_NAME"],
        "IMAGE_KEY": config["IMAGE_KEY"],
        "IMAGE_TYPE": config["IMAGE_TYPE"],
        "IMAGE_ARCH": config["arch"],
        "IMAGE_UUID": config["UUID"],
        "OS_PREFIX": config["OS_PREFIX"],
        "OS_VERSION": config["OS_VERSION"],
        "STREAM": config["stream"],
        "BUILD_FORMAT": config["build_format"],
        "HW_TARGET": config["hw_target"],
        "TESTS_RESULTS_DIR": TESTS_RESULTS_DIR,
        "TMT_PLAN_NAME": results["test"]["fmf"]["name"],
        "TMT_PLAN_PATH": results["test"]["fmf"]["url"],
        "PACKAGE_NAME": config.get("PACKAGE_NAME", ""),  # Not set for product pipelines
        "PACKAGE_NVR": config.get("PACKAGE_NVR", ""),  # Not set for product pipelines
    }
    try:
        with open(ENV_VARS_FILE, "w") as f:
            for key, value in env_vars.items():
                # Add escaped vars to the list below
                if key in ["ARTIFACTS_WORKDIR_URLS"]:
                    f.write(f"{key}='{value}'\n")
                else:
                    f.write(f"{key}={value}\n")
    except IOError as e:
        logging.error(f"File operation error: {e}")
        return

    logging.info(f"ENV variables stored at '{ENV_VARS_FILE}' for future use")


def fail_on_error(results: Dict[str, Any]) -> None:
    """
    Process the API request results and fail if the test didn't run.

    It can fail for known TF error codes (normally infra related issues), or due to unkown reasons.

    Args:
        results (Dict[str, Any]): The structure with the response from the API.
    """
    job_id = results["id"]
    result = results["result"]["overall"]
    summary = results["result"]["summary"]
    report_url = results["run"]["artifacts"]
    logging.info(f"Processing results for the job {job_id}...")
    logging.debug(f"Test result: {result}")

    if result in TEST_ERROR_CODES:
        logging.error(f"There has been an error in Testing Farm with code '{result}'")
        logging.error(f"Error message: {summary}")
        logging.error(f"More details here: {report_url}")

        # Exit with 10 to indicate that the test didn't even run
        # It could mean infra, API, tmt or test error
        sys.exit(10)

    if result not in TEST_VALID_CODES:
        logging.error(f"There has been an uknown error with code '{result}'")
        logging.error(f"Error message: {summary}")
        logging.error(f"More details here: {report_url}")

        # Exit with 15 to indicate that the test didn't even run
        # This is not a known code and we don't know what it means
        sys.exit(15)

    logging.info("The tests have been executed successfully")
    sys.exit(0)


def post_process_results(results: Dict[str, Any], config: Dict[str, Any]) -> None:
    """
    Process the results from the Testing Farm job.

    - Display the result (passed, failed, error or unkown).
    - Store the JUnit report in case of tests (ACTION=TEST).
    - Store some variables in a .env file, so they can be used but the GitLab job.
    - Exit the program with the appropriated exit code:
        - 0: the test ran (either 'passed' or 'failed').
        - 10: the test didn't run. It could be TF error or an error in the test itself (or tmt).
        - 15: the test didn't run. Unkown error.

    Args:
        results (Dict[str, Any]): The structure with the response from the API.
        config (Dict[str, Any]): Variables to be used in different operations by the program.
    """
    display_results(results)

    config["artifacts_workdir_urls"] = json.dumps(get_artifacts_workdir_urls(results))

    if config["action"] == "TEST":
        store_results(results)

    save_env_vars(results, config)
    fail_on_error(results)


def main():
    args = cli()
    secrets, variables, config = load_configuration(args)

    # Check if it's running for images or packages
    if config["action"] == "TEST" and "PACKAGE_NAME" in config:
        # Running test for packages (p-l-p)
        adjust_for_package_testing(config, variables)

        # Check for a special case: tests on physical boards (QDrive3 and such)
        if config["hw_target"] != "aws":
            set_boards_settings(config)
    else:
        # Running builds and integrations tests for images (p-a-c)

        # Set any special options for builds
        if config["action"] == "BUILD":
            config["environments__hardware__disk"] = [{"size": DISK_SIZE_BUILD}]

        # Check for a special case: tests on physical boards (QDrive3 and such)
        if config["hw_target"] != "aws" and config["action"] == "TEST":
            set_boards_settings(config)

        # Check if it's a smoke-test
        if config["action"] == "TEST" and "smoke" in config["test__fmf__name"]:
            # Don't count provision errors as TF errors
            config["settings__pipeline__provision-error-failed-result"] = True
            if config["hw_target"] != "aws":
                # Set some Testing Farm variables to avoid retying the job if the job
                # doesn't run on AWS. Which means that is running on a physical board.
                # Only try to provision once
                config["environments__settings__provisioning__tags__ArtemisOneShotOnly"] = True

        config["tf_compose"] = determine_tf_compose(
            config["tf_compose"],
            config["action"],
            config["IMAGE_KEY"],
            config["arch"],
            config["stream"],
            config["build_format"],
        )

    payload = generate_payload(config, variables, secrets)

    # Show the payload and exit
    if args.show_payload:
        print(to_json_string(payload))
        return

    # Make the actual API call and the rest
    results = make_request_and_wait(config["tf_endpoint"], payload)
    post_process_results(results, config)


if __name__ == "__main__":
    main()
