import os
from time import sleep, time

import numpy as np
import pytest
import requests

import docker

HOST_PORT = os.getenv("HOST_PORT", default=5000)
CONTAINER_PORT = 5000
SERVICE_PREDICT_PATH = os.getenv(
    "SERVICE_PREDICT_PATH",
    default=f"http://localhost:{HOST_PORT}/predict",
)
SERVICE_PING_PATH = os.getenv(
    "SERVICE_PING_PATH",
    default=f"http://localhost:{HOST_PORT}/ping",
)
MAX_WAITING_TIME = 20


def check_service(ping_url):
    start_time = time()
    ping_response = None
    while time() - start_time < MAX_WAITING_TIME:
        try:
            ping_response = requests.get(ping_url)
            break
        except requests.exceptions.RequestException as err:
            sleep(0.1)
            error_msg = err
    if ping_response is None:
        raise requests.exceptions.RequestException(error_msg)


def pytest_addoption(parser):
    parser.addoption(
        "--scope",
        action="store",
        required=False,
        default="class",
        help=("Docker fixture scope (class or function)\n" + "default value -- class."),
    )
    parser.addoption(
        "--image",
        action="store",
        required=False,
        default="",
        help="Image for testing, necessary",
    )


def determine_scope(fixture_name, config):
    scope = config.getoption("--scope")
    if scope not in ("class", "function"):
        raise ValueError("Invalid scope")
    return scope


@pytest.fixture(scope="module")
def image(request):
    return request.config.getoption("--image")


@pytest.fixture(scope=determine_scope)
def docker_setup(image):
    if image == "":
        raise ValueError("Specify image to test.")
    cli = docker.from_env()
    container = cli.containers.run(
        image,
        ports={CONTAINER_PORT: HOST_PORT},
        detach=True,
    )
    yield container
    print(container.logs())
    container.stop()
