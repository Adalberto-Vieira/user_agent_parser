import gzip
import json
from typing import List


class BaseScriptsFunctions:
    @classmethod
    def load_json_data(cls, file_path: str):
        """Open and load the json data"""
        json_data = []
        try:
            with gzip.open(file_path, "rt", encoding="utf-8") as file:
                for line in file:
                    json_data.append(json.loads(line))
            return json_data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(
                f"An error occurred while reading the compressed JSON file: {str(e)}"
            )

    @classmethod
    def save_processed_file(cls, file_path: str, file_data: List):
        try:
            with gzip.open(file_path, "wt", encoding="utf-8") as file:
                json.dump(file_data, file)
            print(f"JSON data saved to {file_path}")
        except Exception as e:
            print(f"An error occurred while saving the JSON data: {str(e)}")
