import pandas as pd
import pytest

import urlclassifier.model as url_model


def test_encode_target():
    test_data = pd.Series(
        [
            "Safe",
            "Malicious",
            "Phishing",
            "Unsafe click",
            "Phishing",
        ]
    )
    test_result = pd.Series([0, 1, 2, 3, 2])
    encoded_target = url_model.encode_target(test_data)
    assert test_result.equals(encoded_target)


class TestURLPreprocessing:
    preprocessing = url_model.URLPreprocessing()

    @pytest.mark.parametrize(
        "ip,expected",
        [("127.0.0.0.0", False), ("127.A.0.0", False), ("575.0.0.1", False), ("127.0.0.1", True)],
    )
    def test_validate_ip(self, ip, expected):
        result = self.preprocessing._validate_ip(ip)
        assert result == expected

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("http://kaspersky.ru", "http"),
            ("https://kaspersky.ru", "https"),
            ("ftp://kaspersky.ru", "other"),
        ],
    )
    def test_scheme_parse(self, url, expected):
        result = self.preprocessing._scheme_parse(url)
        assert result == expected

    def test_extract_features(self):
        test_data = ["https://kaspersky1.ru"]
        expected_result = pd.DataFrame(
            {
                "url_len": [21],
                "scheme": ["https"],
                "digit_cnt": [1],
                "domain_tokens_cnt": [2],
                "ip_as_domain": [False],
            }
        )
        result = self.preprocessing._extract_features(test_data)
        assert result.equals(expected_result)
