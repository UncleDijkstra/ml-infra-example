import pytest
import requests
from conftest import SERVICE_PING_PATH, SERVICE_PREDICT_PATH, check_service

TEST_URLS = [
    "http://kraspersky.com",
    "https://kaspersky.com",
    "http://yandex.ru",
    "https://yandex.ru",
]


TEST_REQUEST_JSONS = [
    TEST_URLS[0],
    TEST_URLS,
]


class TestPredictRequests:
    @staticmethod
    @pytest.mark.parametrize("request_json", TEST_REQUEST_JSONS)
    def test_predict_request(docker_setup, request_json):
        check_service(SERVICE_PING_PATH)

        response = requests.post(SERVICE_PREDICT_PATH, json=request_json)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list):
            result = result[0]
        assert isinstance(result, dict)
        assert "PedictedGroupId" in result
        assert isinstance(result["PedictedGroupId"], int)
