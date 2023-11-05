import os
import gzip
import json
from typing import List

INPUT_PATH = os.path.join("..", "input")
OUTPUT_PATH = os.path.join("..", "output")


class BaseScriptsFunctions:
    @classmethod
    def load_json_data(cls, file_name: str):
        """Open and load the json data"""
        try:
            with gzip.open(
                os.join(INPUT_PATH, file_name), "rt", encoding="utf-8"
            ) as file:
                json_data = json.loads(file.read())
            return json_data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {os.join(INPUT_PATH, file_name)}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON data: {str(e)}")
        except Exception as e:
            raise Exception(
                f"An error occurred while reading the compressed JSON file: {str(e)}"
            )

    @classmethod
    def save_processed_file(cls, file_name: str, file_data: List):
        try:
            with gzip.open(
                os.join(OUTPUT_PATH.file_name), "wt", encoding="utf-8"
            ) as file:
                json.dump(file_data, file)
            print(f"JSON data saved to {file_name}")
        except Exception as e:
            print(f"An error occurred while saving the JSON data: {str(e)}")
