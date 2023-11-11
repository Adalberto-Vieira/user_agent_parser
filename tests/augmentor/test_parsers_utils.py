import pytest
from user_agents import parse


from augmentor.parsers_utils import ParserUtils


class TestParsersUtils:
    TEST_CASES_DEVICE_TYPE = [
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/58.0.3029.110 Safari/537.36",
            "Computer",
        ),
        (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 Version/14.0 Mobile/15E148 Safari/604.1",
            "Mobile",
        ),
        (
            "Mozilla/5.0 (Linux; Android 8.0.0; Pixel Build/OPR3.170623.013) AppleWebKit/537.36 Chrome/58.0.3029.110 Mobile Safari/537.36",
            "Mobile",
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/16.16299 Safari/537.36",
            "Computer",
        ),
        (
            "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 Version/14.0 Mobile/15E148 Safari/604.1",
            "Tablet",
        ),
    ]

    TEST_CASES_USER_AGENT_PARSER = [
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/58.0.3029.110 Safari/537.36",
            {
                "Device Type": "Computer",
                "Browser Type": "Chrome",
                "Browser Version": "58.0.3029",
                "Failure": False,
            },
        ),
        (
            '"Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Mobile/15E148 Safari/604.1"',
            {
                "Device Type": "Mobile",
                "Browser Type": "Mobile Safari",
                "Browser Version": "16.5.2",
                "Failure": False,
            },
        ),
        (
            "Mozilla/5.0 (Linux; Android 8.0.0; Pixel Build/OPR3.170623.013) AppleWebKit/537.36 Chrome/58.0.3029.110 Mobile Safari/537.36",
            {
                "Device Type": "Mobile",
                "Browser Type": "Chrome Mobile",
                "Browser Version": "58.0.3029",
                "Failure": False,
            },
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/16.16299 Safari/537.36",
            {
                "Device Type": "Computer",
                "Browser Type": "Edge",
                "Browser Version": "16.16299",
                "Failure": False,
            },
        ),
        (
            None,
            {
                "Device Type": None,
                "Browser Type": None,
                "Browser Version": None,
                "Failure": True,
            },
        ),
    ]

    @pytest.mark.parametrize(
        "user_agent_str, expected_device_type", TEST_CASES_DEVICE_TYPE
    )
    def test_select_device_type(self, user_agent_str, expected_device_type):
        user_agent = parse(user_agent_str)
        device_type = ParserUtils._select_device_type(user_agent)
        assert device_type == expected_device_type

    @pytest.mark.parametrize(
        "user_agent_str, expected_details", TEST_CASES_USER_AGENT_PARSER
    )
    def test_parse_user_agent(self, user_agent_str, expected_details):
        ua_augmentor = ParserUtils()
        details = ua_augmentor.parse_user_agent(user_agent_str)
        assert details.to_dict() == expected_details
