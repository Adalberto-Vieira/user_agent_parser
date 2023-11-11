import os
import pandas as pd
import pytest
from unittest.mock import patch
from augmentor.user_agent_augmentor import UserAgentAugmentor

INPUT_FILE_PATH = os.path.join("..", "input", "sample_orders.json.gz")
OUTPUT_FILE_PATH = os.path.join("..", "output")
OUTPUT_FILE_NAME = "sample_orders_transformed.json.gz"
USER_AGENT = "USER_AGENT"


class TestUserAgentAugmentor:
    @pytest.fixture
    def user_agent_augmentor_instance(self):
        return UserAgentAugmentor()

    @patch("augmentor.file_utils.FileUtils.load_json_data")
    @patch("augmentor.file_utils.FileUtils.save_processed_file")
    def test_run_method_successful(
        self,
        mock_save_processed_file,
        mock_load_json_data,
        user_agent_augmentor_instance,
        capsys,
    ):
        # Mocking the load_json_data method to return realistic data
        mock_load_json_data.return_value = [
            {
                "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
        ]

        user_agent_augmentor_instance.run()

        # Capture the printed output
        captured = capsys.readouterr()

        # Add assertions based on the expected behavior of the run method
        assert "Started user agent augmentation" in captured.out
        assert "processed 1 rows" in captured.out
        assert "failed to process 0 rows" in captured.out

        # Additional assertions based on the mock calls
        mock_load_json_data.assert_called_once_with(INPUT_FILE_PATH)
        mock_save_processed_file.assert_called_once_with(
            OUTPUT_FILE_PATH,
            OUTPUT_FILE_NAME,
            [
                {
                    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                    "Device Type": "Computer",
                    "Browser Type": "Chrome",
                    "Browser Version": "58.0.3029",
                    "Failure": False,
                }
            ],
        )

    @patch("augmentor.file_utils.FileUtils.load_json_data")
    def test_run_method_exception(
        self, mock_load_json_data, user_agent_augmentor_instance, capsys
    ):
        # Mocking the load_json_data method to raise an exception
        mock_load_json_data.side_effect = Exception("Simulated error loading data")

        user_agent_augmentor_instance.run()

        # Capture the printed output
        captured = capsys.readouterr()

        # Add assertions based on the expected behavior when an exception occurs
        assert (
            "The following error ocurrud: Simulated error loading data\n"
            in captured.out
        )

        # Additional assertions based on the mock calls
        mock_load_json_data.assert_called_once_with(INPUT_FILE_PATH)

    def test_augment_data_method(self, user_agent_augmentor_instance):
        # Mock data for testing
        user_agent_augmentor_instance.df = pd.DataFrame(
            {USER_AGENT: ["user_agent_1", "user_agent_2", "user_agent_3"]}
        )

        user_agent_augmentor_instance._augment_data()

        assert "Device Type" in user_agent_augmentor_instance.df.columns
        assert "Browser Type" in user_agent_augmentor_instance.df.columns
        assert "Browser Version" in user_agent_augmentor_instance.df.columns
        assert "Failure" in user_agent_augmentor_instance.df.columns
