import pandas as pd
import os

from . import file_utils
from . import parsers_utils

INPUT_FILE_PATH = os.path.join("..", "input", "sample_orders.json.gz")
OUTPUT_FILE_PATH = os.path.join("..", "output")
OUTPUT_FILE_NAME = "sample_orders_transformed.json.gz"
USER_AGENT = "USER_AGENT"


class UserAgentAugmentor:
    def __init__(self):
        self._file_functions = file_utils.FileUtils()
        self._parser = parsers_utils.ParserUtils()
        self.df = pd.DataFrame()
        self.total_failures = 0
        self.total_processed_rows = 0

    def run(self):
        print("Started user agent augmentation")
        try:
            self.df = pd.DataFrame.from_records(
                self._file_functions.load_json_data(INPUT_FILE_PATH)
            )
            self._augment_data()
            self._file_functions.save_processed_file(
                OUTPUT_FILE_PATH, OUTPUT_FILE_NAME, self.df.to_dict("records")
            )
            self.total_failures = len(self.df[self.df["Failure"]])
            self.total_processed_rows = len(self.df) - self.total_failures
            print(f"processed {self.total_processed_rows} rows")
            print(f"failed to process {self.total_failures} rows")
        except Exception as e:
            print(f"The following error ocurrud: {e}")

    def _augment_data(self):
        new_columns = self.df[USER_AGENT].apply(self._parser.parse_user_agent)
        self.df[new_columns.columns] = new_columns
