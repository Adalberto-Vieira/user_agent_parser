import pandas as pd
import os
from user_agents import parse

from . import base_script_functions

INPUT_FILE_PATH = os.path.join("..", "input", "sample_orders.json.gz")
OUTPUT_FILE_PATH = os.path.join("..", "output", "sample_orders_transformed.json.gz")
USER_AGENT = "USER_AGENT"


class UserAgentAugmentor:
    def __init__(self):
        self._functions = base_script_functions.BaseScriptsFunctions()
        self.df = pd.DataFrame()
        self.total_failures = 0
        self.total_processed_rows = 0

    def _augment_data(self):
        new_columns = self.df[USER_AGENT].apply(self._parse_user_agent)
        self.df[new_columns.columns] = new_columns

    def _replace_empty_str_with_none(self):
        """
        Replaces instances where the USER_AGENT str is just quotas for None
        """
        self.df = self.df.replace('""', None)

    @classmethod
    def _select_device_type(cls, user_agent):
        if user_agent.is_mobile:
            return "Mobile"
        elif user_agent.is_pc:
            return "Computer"
        elif user_agent.is_tablet:
            return "Tablet"
        return "Other"

    def _parse_user_agent(self, agent_str):
        try:
            user_agent = parse(agent_str)
            details = {
                "Device Type": self._select_device_type(user_agent),
                "Browser Type": user_agent.browser.family,
                "Browser Version": user_agent.browser.version_string,
                "Failure": False,
            }
        except Exception as e:
            details = {
                "Device Type": None,
                "Browser Type": None,
                "Browser Version": None,
                "Failure": True,
            }
            self.total_failures += 1
            print(f"Failed processing of a row with error{e}")
        return pd.Series(details)

    def run(self):
        print("Started user agent augmentation")
        try:
            self.df = pd.DataFrame.from_records(
                self._functions.load_json_data(INPUT_FILE_PATH)
            )
            self._replace_empty_str_with_none()
            self._augment_data()
            self._functions.save_processed_file(
                OUTPUT_FILE_PATH, self.df.to_dict("records")
            )
            print(f"processed {self.total_processed_rows} rows")
            print(f"failed to process {self.total_failures} rows")
        except Exception as e:
            print(f"The following error ocurrud: {e}")
