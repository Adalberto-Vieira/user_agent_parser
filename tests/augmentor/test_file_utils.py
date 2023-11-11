import os
import gzip
import json
import shutil
import pytest

from augmentor.file_utils import FileUtils


class TestFileUtils:
    @classmethod
    def setup_class(cls):
        # Create a temporary test directory for input and output
        cls.test_input_dir = "test_input"
        cls.test_output_dir = "test_output"
        os.makedirs(cls.test_input_dir, exist_ok=True)
        os.makedirs(cls.test_output_dir, exist_ok=True)

    @classmethod
    def teardown_class(cls):
        # Clean up temporary test directories
        shutil.rmtree(cls.test_input_dir, ignore_errors=True)
        shutil.rmtree(cls.test_output_dir, ignore_errors=True)

    def test_load_json_data_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            FileUtils.load_json_data("nonexistent_file.json.gz")

    def test_load_json_data_file_format_error(self):
        # Create a test input file with invalid JSON
        with gzip.open(
            os.path.join(self.test_input_dir, "invalid_data.json.gz"),
            "wt",
            encoding="utf-8",
        ) as file:
            file.write("invalid_json")

        with pytest.raises(Exception):
            FileUtils.load_json_data("invalid_data.json.gz")

    def test_save_processed_file(self):
        # Test data
        test_data = [{"name": "John", "age": 30}, {"name": "Alice", "age": 25}]

        # Save the data
        file_path = os.path.join(self.test_output_dir, "output_data.json.gz")
        FileUtils.save_processed_file(
            self.test_output_dir, "output_data.json.gz", test_data
        )

        assert os.path.isfile(file_path)

    def test_load_and_save_json_data(self):
        # Test data
        test_data = [{"name": "John", "age": 30}, {"name": "Alice", "age": 25}]

        # Save the data
        input_file_path = os.path.join(self.test_output_dir, "test_data.json.gz")
        FileUtils.save_processed_file(
            self.test_output_dir, "test_data.json.gz", test_data
        )

        # Load and save the data
        output_file_path = os.path.join(
            self.test_output_dir, "output_test_data.json.gz"
        )
        loaded_data = FileUtils.load_json_data(input_file_path)
        FileUtils.save_processed_file(
            self.test_output_dir, "output_test_data.json.gz", loaded_data
        )

        # Check if the loaded and saved data match
        with gzip.open(output_file_path, "rt", encoding="utf-8") as file:
            saved_data = json.load(file)
        assert loaded_data == saved_data
